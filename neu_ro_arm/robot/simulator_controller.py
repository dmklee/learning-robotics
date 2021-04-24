import numpy as np
import pybullet as pb

from neu_ro_arm.robot.base_controller import BaseController
from neu_ro_arm.robot.motion_planner import PybulletBase

class SimulatorController(BaseController, PybulletBase):
    def __init__(self):
        PybulletBase.__init__(self, pb.GUI)
        pb.setRealTimeSimulation(1, self._client)
        self.arm_jpos_home = np.zeros(len(self.arm_joint_idxs))
        self.joint_limits =  { 1 : (-3, 3),
                               2 : (-np.pi, np.pi),
                               3 : (-np.pi, np.pi),
                               4 : (-np.pi, np.pi),
                               5 : (-np.pi, np.pi),
                               6 : (-0.3, 0.3),
                               7 : (-0.3, 0.3),
                             }

    def move_command(self, j_idxs, jpos):
        '''Issue move command to specified joint indices

        This simulator runs realtime and I have not tried to mimic the movement
        speed of the real robot.  The movements are meant to be linear in joint
        space to reflect movements of xArm.

        Parameters
        ----------
        j_idxs : array_like of int
            joint indices to be moved
        jpos : array_like of float
            target joint positions corresponding to the joint indices
        '''
        num_joints = len(j_idxs)
        pb.setJointMotorControlArray(self.robot_id,
                                     j_idxs,
                                     pb.POSITION_CONTROL,
                                     jpos,
                                     physicsClientId=self._client
                                    )

    def read_command(self, j_idxs):
        '''Read some joint positions

        Parameters
        ----------
        j_idxs : array_like of int
            joint indices whose position should be read

        Returns
        -------
        jpos : list of float
            joint positions in radians, will be same length as j_idxs
        '''
        jpos = [pb.getJointState(self.robot_id, j_idx, physicsClientId=self._client)[0]
                           for j_idx in j_idxs]
        return jpos

if __name__ == "__main__":
    import time
    arm = SimulatorController()
    # arm.power_off()
    names = ['base', 'shoulder', 'elbow', 'wrist', 'wristRotation']
    while True:
        jpos = arm.read_command(arm.arm_joint_idxs)
        print([f"{n}:{jp:.2f}" for jp,n in zip(jpos, names)])
        # arm.move_command(arm.gripper_joint_idxs, arm.gripper_opened)
        # time.sleep(1)
        # arm.move_command(arm.gripper_joint_idxs, arm.gripper_closed)
        # time.sleep(1)
        # pos = [arm._to_pos_units(jp) for jp in jpos]
        # print([f"{n}:{p}" for p,n in zip(pos, names)])

        # print([f"{a:0.2f}" for a in arm._read_all_servos_pos_angle()])

