/*

  Register event listener so the user can "submit" moves, but client-side validation on whether it's
  actually our turn or not for the sake of simplicity.

 */


const fetch = require('node-fetch')

MOVE_API_ENDPOINT   = 'http://138.68.18.203:8002/tictac/api_makemove/'
STATECHECK_ENDPOINT = 'http://138.68.18.203:8002/tictac/api_checkstate/'
TEST_ENDPOINT = 'http://138.68.18.203:8002/tictac/api_test/'

class View {

  constructor(username, allegiance, active_player, remaining_time) {
    this.username = username
    this.allegiance = allegiance          // 'X' or 'O'
    this.our_turn = false;
    this.pending_promise = false;         // Informs decison to make update requests to the server
    this.remaining_time = remaining_time  // time left for the current player to complete their move

    // Actually determining if it's our turn now
    if (username === active_player) {
      this.our_turn = true;
    }

    // Kick things off waiting for the opponent to make a move
    if (!this.our_turn) {
      this.poll_gamestate();
    }
  }


  async poll_gamestate() {

    function process_server_success(data, view) {
      // This should be receiving json formatted data subsequent to a successful
      // response from the game state endpoint

      // Checking if a move has been made
      view.current_player = data['current_player']
      if (view.current_player === view.username) {
        view.our_turn = true;
      }

      // Calculate timedelta from last_timestamp to calculate and
      // set the time_remaining in our turn.
      // delta = datetime.now() - data['last_timestamp']
      // this.time_remaining = delta
      console.log('This is our data:', data);

      // Update the html elementById S1 through S9 with the values held in data.
      view.pending_promise = false;
      // Now set up the next api call if we are still waiting on the opponent
      if (!view.our_turn) {
        console.log('it\'s still not our turn..setting up to query the api in another 5 seconds');
        setTimeout(view.poll_gamestate(), 5000);
      }

   }
   function process_server_failure(error, view) {
      // Ending up here when the fetch call
      // results in an error.

      view.pending_promise = false;
      console.log('Encountered the following error:', error)

     // At this point I could just continue looping to a request against the server
     // but I want a mechanism that prevents an infinite loop of failed promises.
   }

    if (!this.pending_promise) {
      this.pending_promise = true;
      fetch('http://138.68.18.203:8002/polls/apitest')
          .then(res => res.json())
          .then(data => process_server_success(data, this))
          .catch(error => process_server_failure(error, this));
    }
 }

 async submit_move(data) {
    console.log('hello!')
  }

}


function sa_process_success(data) {
  console.log(data);
}

function sa_process_failure(data) {
  console.log(data);
}
//var ourview = new View('zeratul', 'X', 'kerrigan', 30);

data = {move: "sq1"}
fetch(TEST_ENDPOINT, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
    .then(res => res.json())
    .then(data => sa_process_success(data))
    .catch(error => sa_process_failure(error));





/*

  useful code for testing gameplay state changes through the console
  before implementing the UI further.

 */

// const stdin = process.openStdin()
//
// process.stdout.write('Enter name: ')
//
// stdin.addListener('data', text => {
//   const name = text.toString().trim()
//   console.log('Your name is: ' + name)
//
// })
//

