var game={
  // Start initializing objects, preloading assets and display start screen
  init: function(){
    // Hide all game layers and display the start screen
    $('.gamelayer').hide();
    $('#gamestartscreen').show();

    // Get handler for game canvas and context
    game.canvas=$('#gamecanvas')[0];
    game.context=game.canvas.getContext('2d');
  },
}

$(window).load(function() {
  game.init*(;
});

var levels={
  // Level data
  data:[
    {  // First level
      foreground:'desert-foreground',
      background:'clouds-background',
      entities:[]
    },
    {  // Second level
      foreground:'desert-foreground',
      background:'clouds-background',
      entities[]
    }
  ],
  // Initialize level selection screen
  init:function(){
    var html="";
    for (var i=0; i<levels.data.length; i++) {
      var level=levels.data[i];
      html+= '<input type="button" value="'+(i+1)+'">';
    };
    $('#levelselectscreen').html(html);

    // Set the button click event handlers to load level
    $('#levelselectscreen input').click(function(){
      levels.load(this.value-1);
      $('#levelselectscreen').hide();
    });
  },

  // Load all data and images for a specific level
  load:function(number){
  }
}

init: function(){
  // Initialize objects
  levels.init();

  // Hide all game layers and display the start screen
  $('.gamelayer').hide();
  $('#gamestartscreen').show();

  // Get handler for game canvas and context
  game.canvas=$('#gamecanvas')[0];
  game.context=game.canvas.getContext('2d');
}, 
