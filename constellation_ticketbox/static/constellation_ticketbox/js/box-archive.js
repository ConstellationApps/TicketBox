/* global Handlebars componentHandler url_api_v1_box_closed_tickets */

/* Global ticket state */
var tickets_data;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-archived').html();

$(document).ready(function(){
  /* Start templating */
  getTicket_data();
});

/* Call APIs to get the JSON ticket_data */
function getTicket_data() {
  tickets_data = { tickets: [], user_tickets: [] };
  $.getJSON(url_api_v1_box_closed_tickets, function(tickets){
    for (var i = 0, len = tickets.length; i < len; i++) {
      if (tickets[i].fields.owner == user_id) {
        tickets_data.user_tickets.push({
          title: tickets[i].fields.title,
          timestamp: tickets[i].fields.timestamp,
          status: tickets[i].fields.status,
          id: tickets[i].pk,
          owner: tickets[i].owner,
          author: tickets[i].author,
          url: url_view_ticket.replace(new RegExp('0' + '$'), tickets[i].pk)
        });
      } else if(tickets[i].fields.archived == true) {
        tickets_data.tickets.push({
          title: tickets[i].fields.title,
          timestamp: tickets[i].fields.timestamp,
          status: tickets[i].fields.status,
          id: tickets[i].pk,
          owner: tickets[i].owner,
          author: tickets[i].author,
          url: url_view_ticket.replace(new RegExp('0' + '$'), tickets[i].pk)
        });
      }
    }
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 404) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    })
  .always(function() {
    renderTemplate(tickets_data);
  });
}

/* render compiled handlebars template */
function renderTemplate(tickets_data){
  var template = Handlebars.compile(source);
  $('#ticketsCard').html(template(tickets_data));
  componentHandler.upgradeDom();
}