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

# Da 1 problema definiamo 1 scena.
# Da questa scena, definiamo 5 task:
#   1) Put <obj1> in the <container> 
#   2) Put <obj2> in the <container>
#   3) Put <obj1> at the left of <obj2>
#   4) Put <obj2> to the front of <obj1>
#   5) Put <obj1> to the front of the <container>


# ==== SCENE DEFINITION
object_1 = "popcorn"
object_2 = "cookies"
object_3 = "red_coffee_mug"
object_4 = "moka_pot"
container = "basket"
fixture_1 = "floor"
# fixture_2 = "white_cabinet"

@register_mu(scene_type="floor")
class FloorScene1(InitialSceneTemplates):
    # ** definisci oggetti, regioni iniziali e dove vanno posizionati gli oggetti
    def __init__(self):

        # libero/libero/assets/articulated_objects
        fixture_num_info = {
            fixture_1: 1
        }

        # objects defined in: libero/libero/assets/stable_scanned_objects
        object_num_info = {
            object_1: 1,
            object_2: 1,
            object_3: 1,
            object_4: 1,
            container: 1
        }

        super().__init__(
            workspace_name="floor",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):

        # # == LEFT/FRONT regions (5cm?)
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.20],
                region_name=f"{object_2}_left_region",
                target_name=self.workspace_name,
                region_half_len=0.1,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.1, 0.0],
                region_name=f"{object_1}_front_region",
                target_name=self.workspace_name,
                region_half_len=0.1,
            )
        )
        
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.1, -0.30],
                region_name=f"{container}_front_region",
                target_name=self.workspace_name,
                region_half_len=0.1,
            )
        )

        # == INIT regions

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 1.0],
                region_name=f"{object_1}_init_region",  # popcorn
                target_name=self.workspace_name,
                region_half_len=0.2,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[1.0, 0.0],
                region_name=f"{object_2}_init_region",  # cookies
                target_name=self.workspace_name,
                region_half_len=0.2,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.20, 0.50],
                region_name=f"{object_3}_init_region",
                target_name=self.workspace_name,
                region_half_len=0.2,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.20, 0.75],
                region_name=f"{object_4}_init_region",
                target_name=self.workspace_name,
                region_half_len=0.2,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, -0.0],
                region_name=f"{container}_init_region",
                target_name=self.workspace_name,
                region_half_len=0.2,
                yaw_rotation=(np.pi, np.pi),
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
            ("On", f"{container}_1", f"{fixture_1}_{container}_init_region"),
        ]
        return states
    
def main():
    
    # == Define the goals given the scene
    # 1) 
    register_task_info(
        language=f'pick up the {object_1} and put it in the {container}',
        scene_name='floor_scene1',
        objects_of_interest=[f"{object_1}_1", f"{container}_1"],
        goal_states=[
            ("On", f"{object_1}_1", f"{container}_1"),
        ],
    )
    # 2)
    register_task_info(
        language=f'pick up the {object_2} and put it in the {container}',
        scene_name='floor_scene1',
        objects_of_interest=[f"{object_2}_1", f"{container}_1"],
        goal_states=[
            ("On", f"{object_2}_1", f"{container}_1"),
        ],
    )

    # 3)
    register_task_info(
        language=f'put the {object_1} to the left of the {object_2}',
        scene_name='floor_scene1',
        objects_of_interest=[f"{object_1}_1", f"{object_2}_1"],
        goal_states=[
            ("On", f"{object_1}_1", f"{fixture_1}_{object_2}_left_region"),
        ],
    )

    # 4)
    register_task_info(
        language=f'put the {object_2} to the front of the {object_1}',
        scene_name='floor_scene1',
        objects_of_interest=[f"{object_2}_1", f"{object_1}_1"],
        goal_states=[
            ("On", f"{object_2}_1", f"{fixture_1}_{object_1}_front_region"),
        ],
    )

    # 5)
    register_task_info(
        language=f'put the {object_1} to the front of the {container}',
        scene_name='floor_scene1',
        objects_of_interest=[f"{object_1}_1", f"{container}_1"],
        goal_states=[
            ("On", f"{object_1}_1", f"{fixture_1}_{container}_front_region"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info(folder='/tmp/pddl/ybq_tasks')
    print(bddl_file_names)


if __name__ == "__main__":
    main()
