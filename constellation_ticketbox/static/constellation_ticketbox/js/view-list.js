/* global Handlebars componentHandler url_api_v1_box_list url_view_boxes */

/* Global box state */
var boxes_data;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-box').html();

$(document).ready(function(){
  /* Start templating */
  getBox_data();
});

/* Call APIs to get the JSON box_data */
function getBox_data() {
  boxes_data = { boxes: [] };
  $.getJSON(url_api_v1_box_list, function(boxes){
    for (var i = 0, len = boxes.length; i < len; i++) {
      if(boxes[i].fields.archived == false) {
        boxes_data.boxes.push({
          name: boxes[i].fields.name,
          desc: boxes[i].fields.desc,
          id: boxes[i].pk,
          url: url_view_box.replace(0, boxes[i].pk)
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
    renderTemplate(boxes_data);
  });
}

/* render compiled handlebars template */
function renderTemplate(boxes_data){
  var template = Handlebars.compile(source);
  $('#boxesCard').html(template(boxes_data));
  componentHandler.upgradeDom();
}
