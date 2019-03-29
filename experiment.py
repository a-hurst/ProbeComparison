# -*- coding: utf-8 -*-

__author__ = "Austin Hurst"

import klibs
from klibs import P
from klibs.KLExceptions import TrialException
from klibs.KLUtilities import deg_to_px, pump, flush, show_mouse_cursor, hide_mouse_cursor
from klibs.KLGraphics import fill, flip, blit
from klibs.KLUserInterface import any_key, key_pressed, ui_request
from klibs.KLGraphics import KLDraw as kld
from klibs.KLCommunication import message
from klibs.KLResponseCollectors import KeyPressResponse, Response
from klibs.KLTime import CountDown

import random
import time
import sdl2

from InterfaceExtras import ThoughtProbe, LikertType

MID_RED = (255, 128, 128, 255)
MID_GREEN =  (128, 255, 128, 255)
TRANSPARENT_GREY = (192, 192, 192, 64)


class ProbeComparison(klibs.Experiment):

    def setup(self):

        # Initialize text styles

        self.txtm.add_style('normal', '0.7deg')
        self.txtm.add_style('title', '1.0deg')
        self.txtm.add_style('stream', '1.5deg')

        # Stimulus sizes

        mask_size = deg_to_px(1.5)
        mask_thick = deg_to_px(0.25)
        acc_size = deg_to_px(0.5)
        acc_offset = deg_to_px(3.0)
        arrow_tail_l = deg_to_px(0.5)
        arrow_tail_w = deg_to_px(0.2)
        arrow_head_l = deg_to_px(0.3)
        arrow_head_w = deg_to_px(0.5, even=True)
        box_size = deg_to_px(2.0)
        box_stroke = deg_to_px(0.2)

        # Generate shape stimuli for instructions

        self.arrow = kld.Arrow(arrow_tail_l, arrow_tail_w, arrow_head_l, arrow_head_w)
        self.arrow.fill = P.default_color
        self.target_box = kld.Rectangle(box_size, stroke=[box_stroke, P.default_color])
        
        # Generate shape stimuli for task

        self.accuracy_rect = kld.Rectangle(acc_offset, acc_offset+acc_size*2, fill=P.default_color)
        self.accuracy_mask = kld.Rectangle(acc_offset+2, acc_offset, fill=P.default_fill_color)
        self.mask = kld.Asterisk(mask_size, mask_thick, fill=P.default_color)

        # Select random letters from the alphabet and render for use in task

        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        random.shuffle(alphabet)
        self.letter_set = alphabet[:P.set_size]
        self.letters = {}
        for letter in self.letter_set:
            self.letters[letter] = message(letter, style='stream', blit_txt=False)

        # Initialize thought probes

        self.probe_condition = P.condition_map[P.condition]
        self.probe = self._init_probe(self.probe_condition)

        # Determine proportion of non-nback trials

        is_nback = self.trial_factory.exp_factors['is_target']
        self.nback_rate = sum(is_nback) / len(is_nback)

        # Determine order of difficulty levels (counterbalancing)

        self.first_nback = random.choice([1, 2])

        # Show task instructions and example thought probe

        self.instructions()

        # Add practice blocks to start of task

        if P.run_practice_blocks:
            self.insert_practice_block(1, trial_counts=48)
            self.insert_practice_block(2, trial_counts=48)

    
    def _init_probe(self, probetype):

        p_origin = (P.screen_c[0], P.screen_x//10)

        if probetype == 'christoff2009':
            q = ("What was your attention focused on just before the probe?\n"
                 "1 (on-task) - 7 (off-task)")
            title = message(q, "title", align='center', blit_txt=False)
            return LikertProbe(1, 7, title, int(P.screen_x*0.6), p_origin)

        elif probetype == 'killingsworth2010':
            q = "Are you thinking about something other than\nwhat you're currently doing?"
            responses = {
                'on_task': "No",
                'mw_pleasant': "Yes, something pleasant",
                'mw_neutral': "Yes, something neutral",
                'mw_unpleasant': "Yes, something unpleasant"
            }
            order = ['on_task', 'mw_pleasant', 'mw_neutral', 'mw_unpleasant']
            title = message(q, "title", align='center', blit_txt=False)
            return ThoughtProbe(responses, title, int(P.screen_x*0.6), p_origin, order)

        elif probetype == 'mason2007':
            q = "Were you just having an irrelevant thought?\n\n"
            responses = {
                'irrelevant': "Yes",
                'relevant': "No",
            }
            order = ['irrelevant', 'relevant']
            title = message(q, "title", align='center', blit_txt=False)
            return ThoughtProbe(responses, title, int(P.screen_x*0.6), p_origin, order)

        elif probetype == 'mcvay2009':
            q = "What were you just thinking about?"
            responses = {
                'task': "The task",
                'performance': "Task experience/performance",
                'everyday': "Everyday stuff",
                'currentstate': "Current state of being",
                'worries': "Personal worries",
                'daydreams': "Daydreams",
                'other': "Other"
            }
            order = [
                'task', 'performance', 'everyday', 'currentstate', 'worries',
                'daydreams', 'other'
            ]
            title = message(q, "title", align='center', blit_txt=False)
            return ThoughtProbe(responses, title, int(P.screen_x*0.6), p_origin, order)
        
        elif probetype == 'mrazek2013':
            q = ("To what extent was your attention focused on the task\n"
                 "or to task-unrelated concerns?")
            title = message(q, "title", align='center', blit_txt=False)
            return LikertProbe(1, 5, title, int(P.screen_x*0.45), p_origin)


    def instructions(self):

        p1 = ("During this task, you will presented with a sequence of letters in the middle of "
            "the screen.\n\nPress any key to see an example.")
        p2a = ("For some blocks, your task will be to indicate whether each letter matches "
            "the letter just before it:")
        p2b = ("For others, your task will be to indicate whether each letter matches "
            "the letter two before it:")
        p2c = "(matches for each block type are highlighted)"
        p3 = ("Occasionally, the task will be interrupted by screens asking you about your "
            "focus just prior.\nWhen this happens, please select the most accurate "
            "response using the mouse cursor.\n\nPress any key to see an example.")

        msg1 = message(p1, 'normal', blit_txt=False, align='center')
        msg2a = message(p2a, 'normal', blit_txt=False, wrap_width=int(P.screen_x*0.8))
        msg2b = message(p2b, 'normal', blit_txt=False, wrap_width=int(P.screen_x*0.8))
        msg2c = message(p2c, 'normal', blit_txt=False)
        msg3 = message(p3, 'normal', blit_txt=False, align='center', wrap_width=int(P.screen_x*0.8))

        # First page of instructions

        flush()
        fill()
        blit(msg1, 5, P.screen_c)
        flip()
        any_key(allow_mouse_click=False)

        # Example stimuli

        for letter in (1, 2, 1):
            trialtime = CountDown(2.5)
            while trialtime.counting():
                mask_on = trialtime.elapsed() > 0.5
                stim = self.mask if mask_on else self.letters[self.letter_set[letter]]
                ui_request()
                fill()
                blit(self.accuracy_rect, 5, P.screen_c)
                blit(self.accuracy_mask, 5, P.screen_c)
                blit(stim, 5, P.screen_c)
                flip()
        
        # Task explanation/illustration

        fill()
        blit(msg2a, 8, (P.screen_c[0], int(P.screen_y*0.15)))
        blit(msg2b, 8, (P.screen_c[0], int(P.screen_y*0.45)))
        blit(msg2c, 2, (P.screen_c[0], int(P.screen_y*0.8)))
        self.draw_nback_illustration(int(P.screen_y*0.3), target=5)
        self.draw_nback_illustration(int(P.screen_y*0.6), target=4)
        flip()
        any_key(allow_mouse_click=False)

        # Probe explanation + example probe

        fill()
        blit(msg3, 5, P.screen_c)
        flip()
        any_key()
        self.probe.collect()


    def block(self):

        # Initialize/reset list of previous letters presented

        self.past_letters = []

        # Determine nback difficulty for the block

        even_block = P.block_number % 2 == 0
        if self.first_nback == 1:
            self.nback = 2 if even_block else 1
        else:
            self.nback = 1 if even_block else 2

        # Determine positions of thought probes in trial sequence

        # Probes are pseudo-randomly distributed throughout blocks, with one probe in every set of
        # 30 trials. Probes cannot appear in the first 8 trials of a set, ensuring that probes are
        # at minimum 20 seconds apart.
        self.probe_trials = []
        noprobe_span = [False] * P.noprobe_span
        probe_span = [True] + [False] * P.probe_span
        while len(self.probe_trials) < P.trials_per_block:
            random.shuffle(probe_span)
            self.probe_trials += noprobe_span + probe_span

        # Generate block message

        header = "Block {0} of {1}".format(P.block_number, P.blocks_per_experiment)
        nback_txts = [' ', 'just before it', 'two before it']
        instructions = (
            "During this block, please press the [m] key when a letter matches\nthe letter "
            "{0}, and the [n] key when it does not.".format(nback_txts[self.nback])
        )
        if P.practicing:
            header = "This is a practice block. ({0})".format(header)
            instructions = instructions + "\nYou will be given feedback on your accuracy."
        msg = message(header+"\n\n"+instructions, 'normal', align="center", blit_txt=False)
        start_msg = message("Press the [n] key to start.", 'normal', blit_txt=False)

        # Show block message, and wait for input before staring block

        message_interval = CountDown(2)
        while message_interval.counting():
            ui_request() # Allow quitting during loop
            fill()
            blit(msg, 8, (P.screen_c[0], int(P.screen_y*0.15)))
            self.draw_nback_illustration(P.screen_c[1], target = 5 if self.nback == 1 else 4)
            flip()

        while True:
            if key_pressed('n'):
                break
            fill()
            blit(msg, 8, (P.screen_c[0], int(P.screen_y*0.15)))
            self.draw_nback_illustration(P.screen_c[1], target = 5 if self.nback == 1 else 4)
            blit(start_msg, 5, (P.screen_c[0], int(P.screen_y*0.75)))
            flip()
            
    
    def setup_response_collector(self):

        # Configure ResponseCollector for collecting N-back responses via keyboard

        self.rc.uses([KeyPressResponse])
        self.rc.display_callback = self.stim_callback
        self.rc.terminate_after = [P.trial_duration, klibs.TK_MS]
        self.rc.keypress_listener.interrupts = True
        self.rc.keypress_listener.key_map = {'m': 'match', 'n': 'nonmatch'}


    def trial_prep(self):

        # Determine if current trial is a probe trial or not & set trial flags

        self.probe_trial = False if P.practicing else self.probe_trials[P.trial_number-1]
        self.stim_off = False

        # If target trial, ensure that it is possible for the trial to be a target trial

        if self.is_target == True and len(self.past_letters) < self.nback:
            if P.trial_number < (1-self.nback_rate) * P.trials_per_block:
                raise TrialException('') # Recycles the trial and reshuffles remaining trials
            else:
                # If we can't guarantee that there'll be at least one upcoming non-target
                # trial, don't recycle/reshuffle in order to avoid potential infinite loop
                self.is_target = False
        
        # Choose letter for current trial, based on whether it's a target trial or not

        if self.is_target:
            self.letter = self.past_letters[-self.nback]
        else:
            self.letter = random.choice(self.letter_set)
            # If not a target trial, make sure random letter isn't accidentally an n-back
            if len(self.past_letters) >= self.nback:
                while self.letter == self.past_letters[-self.nback]:
                    self.letter = random.choice(self.letter_set)

        # Specifiy sequence/onsets of events for the trial

        self.evm.register_ticket(['mask_on', P.target_duration])
        self.evm.register_ticket(['trial_end', P.trial_duration])


    def trial(self):

        # Draw initial trial stimuli to screen

        fill()
        blit(self.accuracy_rect, 5, P.screen_c)
        blit(self.accuracy_mask, 5, P.screen_c)
        blit(self.letters[self.letter], 5, P.screen_c)
        flip()

        # Immediately start listening for reponses, removing letter after 500ms

        self.rc.collect()
        response = self.rc.keypress_listener.response()

        # Process collected response before writing to database, showing feedback if practicing

        if response.rt != klibs.TIMEOUT:
            resp, rt = response
            correct_resp = 'match' if self.is_target else 'nonmatch'
            accuracy = int(resp == correct_resp)
            if P.practicing:
                self.accuracy_rect.fill = MID_GREEN if accuracy == True else MID_RED
                self.accuracy_rect.render()
            while self.evm.before('trial_end'):
                ui_request()
                fill()
                blit(self.accuracy_rect, 5, P.screen_c)
                blit(self.accuracy_mask, 5, P.screen_c)
                if self.evm.before('mask_on'):
                    blit(self.letters[self.letter], 5, P.screen_c)
                else:
                    blit(self.mask, 5, P.screen_c)
                flip()
        else:
            resp, rt, accuracy = ['NA', 'NA', 'NA']

        # If probe trial, present MW probe and wait for response + keypress before ending trial

        if self.probe_trial:
            probe_resp, probe_rt = self.probe.collect()
            probe_rt = probe_rt * 1000 # convert seconds to ms
            resume_msg = message("Press the [n] key to continue.", 'title', blit_txt=False)
            while True:
                if key_pressed('n'):
                    break
                fill()
                blit(resume_msg, 5, P.screen_c)
                flip()
            self.past_letters = []
        else:
            probe_resp, probe_rt = ('NA', 'NA')
            self.past_letters.append(self.letter)

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "practice": P.practicing,
            "probe_type": self.probe_condition,
            "first_nback": self.first_nback,
            "nback": self.nback,
            "target_trial": self.is_target,
            "resp": resp,
            "accuracy": accuracy,
            "rt": rt,
            "probe_resp": probe_resp,
            "probe_rt": probe_rt
        }


    def trial_clean_up(self):

        if P.practicing:
            self.accuracy_rect.fill = P.default_color
            self.accuracy_rect.render()


    def clean_up(self):
        pass


    def draw_nback_illustration(self, yloc, target):

        stims = {
            "A": message("A", 'stream', blit_txt=False),
            "B": message("B", 'stream', blit_txt=False),
            "C": message("C", 'stream', blit_txt=False),
            "->": self.arrow.render()
        }
        stim_sequence = ['A', '->', 'B', '->', 'C', '->', 'B', '->', 'B']
        stim_spacing = deg_to_px(2.5)

        for i in range(0, len(stim_sequence)):
            s = stim_sequence[i]
            midpoint = len(stim_sequence)/2.0 + 0.5
            x_offset = int(stim_spacing * (i+1 - midpoint))
            y_offset = 4 if s == '->' else 0 # fixes arrow offsets
            blit(stims[s], 5, (P.screen_c[0]+x_offset, yloc+y_offset))
            if (i+2)/2.0 == target:
                blit(self.target_box, 5, (P.screen_c[0]+x_offset+1, yloc+3))


    def stim_callback(self):
        
        if not self.stim_off and self.evm.after('mask_on'):
            fill()
            blit(self.accuracy_rect, 5, P.screen_c)
            blit(self.accuracy_mask, 5, P.screen_c)
            blit(self.mask, 5, P.screen_c)
            flip()
            self.stim_off == True



class LikertProbe(object):

    def __init__(self, first, last, question, width, origin):

        self.q = question
        self.width = width
        self.origin = origin

        height = width / (len(range(first, last+1)) + 2)
        self.scale = LikertType(first, last, width, height, style='normal')

    def collect(self):

        show_mouse_cursor()
        onset = time.time()

        while self.scale.response == None:
            q = pump(True)
            ui_request(queue=q)
            fill()
            blit(self.q, location=self.origin, registration=8)
            self.scale.response_listener(q)
            flip()

        response = self.scale.response
        rt = time.time() - onset
        hide_mouse_cursor()
        self.scale.response = None # reset for next time
        return Response(response, rt)
