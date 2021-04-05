// Connects python and javascript over bridge eel

// JAVASCRIPT -> PYTHON
// The onclick functions inside the html file execute these functions. They execute python scripts.

// WORKING
function enter_room(room_name) {
    eel.connect_button_pressed()
    eel.enter_room(room_name)
}


// TODO:
function close_program() {
    eel.close_program()
}
function mute_button_pressed() {
  eel.mute_button_pressed()
}

function deaf_button_pressed() {
    eel.deaf_button_pressed()
}

