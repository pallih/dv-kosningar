var questions = $( ".question-list li.question" )
  .map(function () {
    var id = this.id.replace( /spurning_/, '' );
    var title = $('h1', this).text().replace( /\s+/, ' ' ).trim();
    var name = $( '.choices-list li input[type="radio"]:first', this ).attr( 'name' );
    var opts = $( '.choices-list li label', this )
          .map(function(a,b){
            var t = this.textContent.trim();
            if ( t !== "---------" ) {
              return {
                'id':1
              , 'title': t
              };
            }
            return null;
          })
          .get()
          ;
    var note = $('p', this).text().replace( /\s+/, ' ' ).trim();
    return {
      'id': id
    , 'title': title
    , 'name': name
    , 'note': note
    , 'choices': opts
    };
  })
  .get()
  ;
JSON.stringify( questions, null, 2 );




