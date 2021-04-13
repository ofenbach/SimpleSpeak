// Connects python and javascript over bridge eel

// JAVASCRIPT -> PYTHON
// The onclick functions inside the html file execute these functions. They execute python scripts.

// WORKING
function enter_room(room_name) {
    //eel.connect_button_pressed()
    eel.update_users()
}


eel.expose(update_users_view)
function update_users_view(users_connect, users_room1, users_room2, users_room3) {

    // Clean up old view
    var parent = document.getElementById("container-online-users");
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }

    // DISPLAY USER AMOUNT
    var text = document.getElementById("users_online_text");
    text.innerText = "Users online:";

    // Display new line for each user
    var users_list = users_connect.split(',');
    var arrayLength = users_list.length;
    for (var i = 0; i < arrayLength; i++) {

        // Clean up username
        var username = String(users_list[i])
        username = username.replace('[','');
        username = username.replace(']','');
        username = username.replace("'", "")
        username = username.replace("'", "")

        // Append username
        var h = document.createElement("H1")           // Create a <h1> element
        h.className = "online-user-text";
        var t = document.createTextNode(username);     // Create a text node
        h.appendChild(t);                              // Append the text to <h1>
        parent.appendChild(h);

    }

    // Show dictionairy users in divs
    //var users_div = document.getElementById("room1_users");
    //users_div.innerText = users_room1

    // Show dictionairy users in divs
    //var users_div = document.getElementById("room2_users");
    //users_div.innerText = users_room2

    // Show dictionairy users in divs
    //var users_div = document.getElementById("room3_users");
    //users_div.innerText = users_room3

}

// When a user clicks a button to join a room, highlight this button
eel.expose(update_room_selection)
function update_room_selection(room_name) {

    // Remove every other selection
    let i = 1;
    while (i <= 3 ) {
        var roomname = "room"+i+"_button"
        var room_notselected= document.getElementById(roomname);

        // Select room
        room_notselected.style.backgroundColor = "white";
        room_notselected.style.color = "#9c98a6";
        i++;
    }

    // Select room
    var room_selected = document.getElementById(room_name+"_button");
    room_selected.style.backgroundColor = "#1565D8";
    room_selected.style.color = "white";

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

