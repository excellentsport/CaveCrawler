import sys
import time
import random
import json
import title_screen


def slow_type(t):
    typing_speed = 2000
    # wpm
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)


def get_input(valid_input: list):
    while True:
        user_entered = input()
        if user_entered not in valid_input:
            print("Invalid input. Please use one of the following inputs:\n")
            print(valid_input)
            user_entered = None
        else:
            return user_entered


def display_page_text(lines: list):
    for line in lines:
        slow_type(line + '\n')
        # Make the user press enter to see the next line
        get_input([''])

    
def get_response(options: list):
    print('\nWhat do you do next?')
    time.sleep(0.5)
    for index, option in enumerate(options):
        print(str(index) + ". " + option['option_text'])
    valid_inputs = [str(num) for num in range(len(options))]

    option_index = int(get_input(valid_inputs))

    return option_index


def act_on_option(response_index, options):
    display_page_text(options[response_index]['result_lines'])
    
    global HEALTH_POINTS
    HEALTH_POINTS += options[response_index]['health_change']
    if options[response_index]['health_change'] < 0:
        display_page_text([
            'You have lost health!',
            'You now have ' + str(HEALTH_POINTS) + ' health.'])
    if options[response_index]['health_change'] > 0:
        display_page_text(['You have gained health!', 'You now have ' +
                          str(HEALTH_POINTS) + ' health.'])
    return

def load_story():
    with open('story.json', encoding="utf-8") as file:
        return json.load(file)

def story_flow():
    story = load_story()
    for chapter_index, chapter in enumerate(story):
        for scene_index, scene in enumerate(story[chapter]):
            display_page_text(story[chapter][scene]['lines'])
            
            while True:
                response_index = get_response(story[chapter][scene]['options'])
                act_on_option(response_index, story[chapter][scene]['options'])
                if HEALTH_POINTS <= 0:
                        print('You have died! Better luck next time.')
                        return
                if story[chapter][scene]['options'][response_index]['next_scene'] == 1:
                        break


def y_n_validation(input_text):
    if input_text is 'n':
        return 0
    if input_text is 'y':
        return 1
    else:
        print('Not a valid option. Please enter either y or n.')


if __name__ == '__main__':
    while True:
        HEALTH_POINTS = 20
        print(title_screen.ascii_title)
        time.sleep(2)
        input(title_screen.intro_text)
        story_flow()
        continue_response = y_n_validation(input('Would you like to try again? y/n'))
        if continue_response == 0:
            print('\nThanks for playing.')
            break
        if continue_response == 1:
            print('\n\n')
            continue
    
            
