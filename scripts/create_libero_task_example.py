"""This is a standalone file for create a task in libero."""
import numpy as np

from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    get_task_info,
    generate_bddl_from_task_info,
)

import argparse
parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('-d', '--debug',
                    action='store_true')  # on/off flag
args = parser.parse_args()

if args.debug:
    import debugpy
    debugpy.listen(5678)
    print('wait for client')
    debugpy.wait_for_client()


# from libero.libero.utils.mu_utils import MU_DICT, SCENE_DICT
# from libero.libero.utils.task_generation_utils import TASK_INFO

@register_mu(scene_type="kitchen")
class KitchenScene1(InitialSceneTemplates):
    def __init__(self):

        fixture_num_info = {
            "kitchen_table": 1,
            "wooden_cabinet": 1,
        }

        object_num_info = {
            "akita_black_bowl": 1,
            "ketchup": 1,
        }

        super().__init__(
            workspace_name="kitchen_table",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, -0.30],
                region_name="wooden_cabinet_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
                yaw_rotation=(np.pi, np.pi),
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.0],
                region_name="akita_black_bowl_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.25],
                region_name="ketchup_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )
        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    @property
    def init_states(self):
        states = [
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),
            ("On", "ketchup_1", "kitchen_table_ketchup_init_region"),
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
        ]
        return states


object_1 = "basket"
object_2 = "cookies"
fixture_1 = "floor"
fixture_2 = "white_cabinet"

@register_mu(scene_type="floor")
class FloorScene1(InitialSceneTemplates):
    # ** definisci oggetti, regioni iniziali e dove vanno posizionati gli oggetti
    def __init__(self):

        # libero/libero/assets/articulated_objects
        fixture_num_info = {
            fixture_1: 1,
            fixture_2: 1,
        }

        # objects defined in: libero/libero/assets/stable_scanned_objects
        object_num_info = {
            object_1: 1,
            object_2: 1,
        }

        super().__init__(
            workspace_name="floor",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):

        # left and right regions of {fixture_2} object.

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, -0.25],
                region_name=f"{fixture_2}_right_region",
                target_name=self.workspace_name,
                region_half_len=0.05,
                yaw_rotation=(np.pi, np.pi),
            )
        )
        

        # init regions

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, -0.30],
                region_name=f"{fixture_2}_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
                yaw_rotation=(np.pi, np.pi),
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.0],
                region_name=f"{object_1}_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.25],
                region_name=f"{object_2}_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )
        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    @property
    def init_states(self):
        states = [
            ("On", f"{object_1}_1", f"{fixture_1}_{object_1}_init_region"),
            ("On", f"{object_2}_1", f"{fixture_1}_{object_2}_init_region"),
            ("On", f"{fixture_2}_1", f"{fixture_1}_{fixture_2}_init_region"),
        ]
        return states




def main():
    # kitchen_scene_1
    # ** definisci gli oggetti di interesse, la scena e i goals
    scene_name = "kitchen_scene1"
    language = "Your Language 1"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_cabinet_1", "akita_black_bowl_1"],
        goal_states=[
            ("Open", "wooden_cabinet_1_top_region"),
            ("In", "akita_black_bowl_1", "wooden_cabinet_1_top_region"),
        ],
    )

    # == kitchen scene 2 
    # scene_name = "kitchen_scene1"
    # language = "Your Language 2"
    # register_task_info(
    #     language,
    #     scene_name=scene_name,
    #     objects_of_interest=["wooden_cabinet_1", "akita_black_bowl_1"],
    #     goal_states=[
    #         ("Open", "wooden_cabinet_1_top_region"),
    #         ("In", "akita_black_bowl_1", "wooden_cabinet_1_bottom_region"),
    #     ],
    # )


    # == floor scene 1

    register_task_info(
        language='open the top region of the white cabinet and put the basket in it',
        scene_name='floor_scene1',
        objects_of_interest=['white_cabinet_1', 'basket_1'],
        goal_states=[
            ("Open", "white_cabinet_1_top_region"),
            ("In", "basket_1", "white_cabinet_1_top_region"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()


