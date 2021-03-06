# Based on Chris Campbell's tutorial from iforce2d.net:
# http://www.iforce2d.net/b2dtut/top-down-car

import math


class TDGroundArea(object):
    """
    An area on the ground that the car can run over
    """

    def __init__(self, friction_modifier):
        self.friction_modifier = friction_modifier


class TDTire(object):

    def __init__(self, car, angle, max_drive_force=150,
                 turn_torque=15, max_lateral_impulse=3,
                 dimensions=(0.5, 1.25), density=1.0,
                 position=(0, 0)):

        world = car.body.world

        self.current_traction = 1
        self.turn_torque = turn_torque
        self.max_drive_force = max_drive_force
        self.max_lateral_impulse = max_lateral_impulse
        self.ground_areas = []

        self.body = world.CreateDynamicBody(position=position)
        self.body.CreatePolygonFixture(box=dimensions, density=density)
        self.body.userData = {'obj': self}
        self.body.angle = math.radians(angle)

    @property
    def forward_velocity(self):
        body = self.body
        current_normal = body.GetWorldVector((0, 1))
        return current_normal.dot(body.linearVelocity) * current_normal

    @property
    def lateral_velocity(self):
        body = self.body

        right_normal = body.GetWorldVector((1, 0))
        return right_normal.dot(body.linearVelocity) * right_normal

    def update_friction(self):
        impulse = -self.lateral_velocity * self.body.mass
        if impulse.length > self.max_lateral_impulse:
            impulse *= self.max_lateral_impulse / impulse.length

        self.body.ApplyLinearImpulse(self.current_traction * impulse,
                                     self.body.worldCenter, True)

        aimp = 0.1 * self.current_traction * \
            self.body.inertia * -self.body.angularVelocity
        self.body.ApplyAngularImpulse(aimp, True)

        current_forward_normal = self.forward_velocity
        current_forward_speed = current_forward_normal.Normalize()

        drag_force_magnitude = -2 * current_forward_speed
        self.body.ApplyForce(self.current_traction * drag_force_magnitude * current_forward_normal,
                             self.body.worldCenter, True)

    def update_drive(self, desired_speed):
        if desired_speed == 0:
            return

        # find the current speed in the forward direction
        current_forward_normal = self.body.GetWorldVector((0, 1))
        current_speed = self.forward_velocity.dot(current_forward_normal)

        # apply necessary force
        force = 0.0
        if desired_speed > current_speed:
            force = self.max_drive_force
        elif desired_speed < current_speed:
            force = -self.max_drive_force
        else:
            return

        self.body.ApplyForce(self.current_traction * force * current_forward_normal,
                             self.body.worldCenter, True)

    def update_traction(self):
        friction_coeffecients = []
        for contact_edge in self.body.contacts:
            entity = contact_edge.other.userData.get('entity', None)
            if hasattr(entity, 'friction'):
                friction_coeffecients.append(entity.friction)
           
        if len(friction_coeffecients) > 0:
            self.current_traction = max(friction_coeffecients)
        else:
            self.current_traction = 1

    def set_awake(self, awake):
        self.body.awake = awake

class TDCar(object):
    # vertices = [(1.5, 0.0),
    #             (3.0, 2.5),
    #             (2.8, 5.5),
    #             (1.0, 10.0),
    #             (-1.0, 10.0),
    #             (-2.8, 5.5),
    #             (-3.0, 2.5),
    #             (-1.5, 0.0),
    #             ]

    vertices = [(3.0, 5.0),
                (-3.0, 5.0),
                (-3.0, -5.0),
                (3.0, -5.0)]

    tire_anchors = [(-2.5, -4),
                    (2.5, -4),
                    (-2.5, 8.50-5),
                    (2.5, 8.50-5),
                    ]

    def __init__(self, world, angle = 90, entity=None, vertices=None,
                 tire_anchors=None, density=0.1, position=(0, 0),
                 **tire_kws):

        angle = angle - 90

        if vertices is None:
            vertices = TDCar.vertices

        self.body = world.CreateDynamicBody(position=position)
        self.body.CreatePolygonFixture(vertices=vertices, density=density)
        self.body.userData = {'obj': self, 'entity': entity}
        self.body.angle = math.radians(angle)

        self.tires = [TDTire(self,angle=angle, **tire_kws) for i in range(4)]

        if tire_anchors is None:
            anchors = TDCar.tire_anchors

        joints = self.joints = []
        for tire, anchor in zip(self.tires, anchors):
            j = world.CreateRevoluteJoint(bodyA=self.body,
                                          bodyB=tire.body,
                                          localAnchorA=anchor,
                                          # center of tire
                                          localAnchorB=(0, 0),
                                          enableMotor=False,
                                          maxMotorTorque=1000,
                                          enableLimit=True,
                                          lowerAngle=0,
                                          upperAngle=0,
                                          )

            tire.body.position = self.body.worldCenter + self.body.GetWorldVector(anchor)

            joints.append(j)

    def set_awake(self, awake):
        for w in self.tires:
            w.set_awake(awake)
        self.body.awake = awake

    def update(self, steering_angle, desired_speed, hz):
        for tire in self.tires:
            tire.update_traction()
            tire.update_friction()

        for tire in self.tires:
            tire.update_drive(desired_speed)

        # control steering
        lock_angle = 40

        if steering_angle > lock_angle:
            steering_angle = lock_angle
        elif steering_angle < -lock_angle:
            steering_angle = -lock_angle

        # from lock to lock in 0.5 sec
        turn_speed_per_sec = math.radians(160.)
        turn_per_timestep = turn_speed_per_sec / hz

        desired_angle = math.radians(steering_angle)

        front_left_joint, front_right_joint = self.joints[2:4]
        angle_now = front_left_joint.angle
        angle_to_turn = desired_angle - angle_now

        # TODO fix b2Clamp for non-b2Vec2 types
        if angle_to_turn < -turn_per_timestep:
            angle_to_turn = -turn_per_timestep
        elif angle_to_turn > turn_per_timestep:
            angle_to_turn = turn_per_timestep

        new_angle = angle_now + angle_to_turn
        # Rotate the tires by locking the limits:
        front_left_joint.SetLimits(new_angle, new_angle)
        front_right_joint.SetLimits(new_angle, new_angle)


# class TopDownCar (Framework):
#     name = "Top Down Car"
#     description = "Keys: accel = w, reverse = s, left = a, right = d"
#
#     def __init__(self):
#         super(TopDownCar, self).__init__()
#         # Top-down -- no gravity in the screen plane
#         self.world.gravity = (0, 0)
#
#         self.key_map = {Keys.K_w: 'up',
#                         Keys.K_s: 'down',
#                         Keys.K_a: 'left',
#                         Keys.K_d: 'right',
#                         }
#
#         # Keep track of the pressed keys
#         self.pressed_keys = set()
#
#         # The walls
#         boundary = self.world.CreateStaticBody(position=(0, 20))
#         boundary.CreateEdgeChain([(-30, -30),
#                                   (-30, 30),
#                                   (30, 30),
#                                   (30, -30),
#                                   (-30, -30)]
#                                  )
#
#         # A couple regions of differing traction
#         self.car = TDCar(self.world)
#         gnd1 = self.world.CreateStaticBody(userData={'obj': TDGroundArea(0.5)})
#         fixture = gnd1.CreatePolygonFixture(
#             box=(9, 7, (-10, 15), math.radians(20)))
#         # Set as sensors so that the car doesn't collide
#         fixture.sensor = True
#
#         gnd2 = self.world.CreateStaticBody(userData={'obj': TDGroundArea(0.2)})
#         fixture = gnd2.CreatePolygonFixture(
#             box=(9, 5, (5, 20), math.radians(-40)))
#         fixture.sensor = True
#
#     def Keyboard(self, key):
#         key_map = self.key_map
#         if key in key_map:
#             self.pressed_keys.add(key_map[key])
#         else:
#             super(TopDownCar, self).Keyboard(key)
#
#     def KeyboardUp(self, key):
#         key_map = self.key_map
#         if key in key_map:
#             self.pressed_keys.remove(key_map[key])
#         else:
#             super(TopDownCar, self).KeyboardUp(key)
#
#     def handle_contact(self, contact, began):
#         # A contact happened -- see if a wheel hit a
#         # ground area
#         fixture_a = contact.fixtureA
#         fixture_b = contact.fixtureB
#
#         body_a, body_b = fixture_a.body, fixture_b.body
#         ud_a, ud_b = body_a.userData, body_b.userData
#         if not ud_a or not ud_b:
#             return
#
#         tire = None
#         ground_area = None
#         for ud in (ud_a, ud_b):
#             obj = ud['obj']
#             if isinstance(obj, TDTire):
#                 tire = obj
#             elif isinstance(obj, TDGroundArea):
#                 ground_area = obj
#
#         if ground_area is not None and tire is not None:
#             if began:
#                 tire.add_ground_area(ground_area)
#             else:
#                 tire.remove_ground_area(ground_area)
#
#     def BeginContact(self, contact):
#         self.handle_contact(contact, True)
#
#     def EndContact(self, contact):
#         self.handle_contact(contact, False)
#
#     def Step(self, settings):
#         self.car.update(self.pressed_keys, settings.hz)
#
#         super(TopDownCar, self).Step(settings)
#
#         tractions = [tire.current_traction for tire in self.car.tires]
#         self.Print('Current tractions: %s' % tractions)
#
# if __name__ == "__main__":
#     main(TopDownCar)
