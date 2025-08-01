```bash

# folder: /tmp/pddl/ybq_tasks
# FLOOR_SCENE1_pick_up_the_cookies_and_put_it_in_the_basket.bddl
# FLOOR_SCENE1_put_the_popcorn_to_the_front_of_the_basket.bddl
# FLOOR_SCENE1_pick_up_the_popcorn_and_put_it_in_the_basket.bddl
# FLOOR_SCENE1_put_the_popcorn_to_the_left_of_the_cookies.bddl
# FLOOR_SCENE1_put_the_cookies_to_the_front_of_the_popcorn.bddl


python3 collect_demonstration.py \
	--device=keyboard \
	--num-demonstration=50 \
	--pos-sensitivity=1.0 \
	--rot-sensitivity=1.0 \
	--bddl-file=/tmp/pddl/ybq_tasks/FLOOR_SCENE1_pick_up_the_cookies_and_put_it_in_the_basket.bddl


```