### Klibs Parameter overrides ###

#########################################
# Runtime Settings
#########################################
collect_demographics = True
manual_demographics_collection = False
manual_trial_generation = False
run_practice_blocks = True
multi_user = False
view_distance = 57 # in centimeters, 57cm = 1 deg of visual angle per cm of screen

#########################################
# Available Hardware
#########################################
eye_tracker_available = False
eye_tracking = False

#########################################
# Environment Aesthetic Defaults
#########################################
default_fill_color = (96, 96, 96, 255)
default_color = (255, 255, 255, 255)
default_font_size = 0.6
default_font_unit = 'deg'
default_font_name = 'Hind-Medium'

#########################################
# EyeLink Settings
#########################################
manual_eyelink_setup = False
manual_eyelink_recording = False

saccadic_velocity_threshold = 20
saccadic_acceleration_threshold = 5000
saccadic_motion_threshold = 0.15

#########################################
# Experiment Structure
#########################################
multi_session_project = False
trials_per_block = 270
blocks_per_experiment = 2
table_defaults = {}
conditions = [ # The study to use the probe style from
    'a', # Christoff et al. (2009) [Likert-type, 1-7]
    'b', # Killingsworth et al. (2010) [4-AFC, mood-focused]
    'c', # Mason et al. (2007) [2-AFC]
    'd', # McVay et al. (2009) [7-AFC, content-focused]
    'e'  # Mrazek et al. (2013) [Likert-type, 1-5]
]
condition_map = {
    'a': 'christoff2009',
    'b': 'killingsworth2010',
    'c': 'mason2007',
    'd': 'mcvay2009',
    'e': 'mrazek2013'
}
default_condition = 'c'

#########################################
# Development Mode Settings
#########################################
dm_auto_threshold = True
dm_trial_show_mouse = True
dm_ignore_local_overrides = False
dm_show_gaze_dot = True

#########################################
# Data Export Settings
#########################################
primary_table = "trials"
unique_identifier = "userid"
exclude_data_cols = ["created"]
append_info_cols = ["random_seed"]
datafile_ext = ".txt"

#########################################
# PROJECT-SPECIFIC VARS
#########################################
target_duration = 500 # ms
trial_duration = 2500 # ms
set_size = 10 # number of unique letters used in task

# trials_per_block should be a multiple of probe_span + noprobe_span
probe_span = 22 
noprobe_span = 8 # minimum trials between probes
