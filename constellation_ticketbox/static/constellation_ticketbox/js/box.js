/* global Handlebars componentHandler url_api_v1_box_open_tickets url_view_box 
   url_api_v1_ticket_create */

/* Global ticket state */
var tickets_data;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-tickets').html();

$(document).ready(function(){
  /* Start templating */
  getTicket_data();
});

/* Call APIs to get the JSON ticket_data */
function getTicket_data() {
  tickets_data = { tickets: [], user_tickets: [] };
  $.getJSON(url_api_v1_box_open_tickets, function(tickets){
    for (var i = 0, len = tickets.length; i < len; i++) {
      if (tickets[i].fields.owner == user_id) {
        tickets_data.user_tickets.push({
          title: tickets[i].fields.title,
          timestamp: (new Date(tickets[i].fields.timestamp)).toLocaleString(),
          status: tickets[i].fields.status,
          id: tickets[i].pk,
          url: url_view_ticket.replace(new RegExp('0' + '$'), tickets[i].pk)
        });
      } else if(tickets[i].fields.archived == false) {
        tickets_data.tickets.push({
          title: tickets[i].fields.title,
          timestamp: (new Date(tickets[i].fields.timestamp)).toLocaleString(),
          status: tickets[i].fields.status,
          id: tickets[i].pk,
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

$('#newTicketForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  var form_data = $('#newTicketForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    var ticket = {};
    response = response[0];
    ticket.id = response.pk;
    ticket.title = response.fields.title;
    ticket.timestamp = (new Date(response.fields.timestamp)).toLocaleString();
    ticket.status = response.fields.status;
    ticket.url = url_view_ticket.replace(new RegExp('0' + '$'), response.pk);
    tickets_data.user_tickets.push(ticket);
    renderTemplate(tickets_data);
  }, 'json')
    .fail(function(jqXHR) {
      if (jqXHR.status == 400 || jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    })
    .always(function() {
      form_data.trigger('reset');
    });
}
