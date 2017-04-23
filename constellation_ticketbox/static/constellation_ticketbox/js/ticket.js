/* global Handlebars componentHandler url_api_v1_ticket_replies url_view_ticket
   url_api_v1_reply_create*/

/* Global ticket state */

var replies_data;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-replies').html()

$(document).ready(function(){
  /* Start templating */
  getTicket_data();
});

/* Call APIs to get the JSON replies_data */
function getTicket_data() {
  replies_data = { replies: [] };
  $.getJSON(url_api_v1_ticket_replies, function(replies){
    for (var i = 0, len = replies.length; i < len; i++) {
      if(true) {
        replies_data.replies.push({
          owner: replies[i].fields.owner,
          timestamp: (new Date(replies[i].fields.timestamp)).toLocaleString(),
          body: replies[i].fields.body,
          anonymous: replies[i].fields.anonymous,
          is_action: replies[i].fields.is_action
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
    renderTemplate(replies_data);
  });
}

/* render compiled handlebars template */
function renderTemplate(replies_data){
  var template = Handlebars.compile(source);
  $('#repliesCard').html(template(replies_data));
  componentHandler.upgradeDom();
}

$('#newReplyForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  var form_data = $('#newReplyForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    var reply = {};
    response = response[0];
    reply.id = response.pk;
    reply.body = response.fields.body;
    reply.owner = response.fields.owner;
    reply.timestamp = (new Date(response.fields.timestamp)).toLocaleString();
    reply.anonymous = response.fields.anonymous;
    reply.is_action = response.fields.is_action;
    replies_data.replies.push(reply);
    renderTemplate(replies_data);
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

