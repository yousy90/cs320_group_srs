

const fetch = require('node-fetch')

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

    // Call the fetch function here to get things going?
    if (!this.our_turn) {
      console.log('It isn\'t our turn');
      this.poll_gamestate();
    }
  }

 async poll_gamestate() {

    function process_server_success(data, view) {
      // This should be receiving json formatted data subsequent to a successful
      // response from the game state endpoint
      view.current_player = data['current_player']
      if (view.current_player === view.username) {
        view.our_turn = true;
      }
      // Calculate timedelta from last_timestamp to calculate and
      // set the time_remaining in our turn.
      // delta = datetime.now() - data['last_timestamp']
      // this.time_remaining = delta
      view.pending_promise = false;
      console.log('This is our data:', data);

      // Now set up the next api call if we are still waiting on the opponent
      if (!view.our_turn) {
        console.log('it\'s still our turn..setting up to query the api in another 5 seconds');
        setTimeout(view.poll_gamestate(), 5000);
      }
   }
   function process_server_failure(error, view) {
      // Ending up here when the fetch call
      // results in an error.
      view.pending_promise = false;
      console.log('Encountered the following error:', error)
   }

    if (!this.pending_promise) {
      this.pending_promise = true;
      fetch('http://138.68.18.203:8002/polls/apitest')
          .then(res => res.json())
          .then(data => process_server_success(data, this))
          .catch(error => process_server_failure(error, this));
    }
 }

}


var ourview = new View('zeratul', 'X', 'kerrigan', 30);

console.log('here');

