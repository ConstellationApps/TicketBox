/* global Handlebars componentHandler url_api_v1_box_list
   url_view_box url_api_v1_box_create url_api_v1_box_edit*/

/* Global box state */
var boxes_data;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-box').html();

$(document).ready(function(){
  /* Start templating */
  getBox_data();
});

/* Call APIs to get the JSON Box_data */
function getBox_data() {
  boxes_data = { active_boxes: [], inactive_boxes: [] };
  $.getJSON(url_api_v1_box_list, function(boxes){
    for (var i = 0, len = boxes.length; i < len; i++) {
      var box_array;
      if(boxes[i].fields.archived == false) {
        box_array = boxes_data.active_boxes;
      } else {
        box_array = boxes_data.inactive_boxes;
      }
      box_array.push({
        name: boxes[i].fields.name,
        id: boxes[i].pk,
        url: url_view_box.replace(0, boxes[i].pk)
      });
    }
    renderTemplate(boxes_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 404) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

/* render compiled handlebars template */
function renderTemplate(boxes_data){
  var template = Handlebars.compile(source);
  $('#boxesCard').html(template(boxes_data));
  componentHandler.upgradeDom();
}

/* edit a box */
function editBox(id) {
  window.location.href = url_box_edit.replace(0, id);
}



/* archive a box */
function archiveBox(id) {
  $.get(url_api_v1_box_archive.replace(0, id), function(){
    var box_index = boxes_data.active_boxes.findIndex(function(element){
      return element.id == id;
    });
    boxes_data.inactive_boxes.push(boxes_data.active_boxes[box_index]);
    boxes_data.active_boxes.splice(box_index, 1);
    renderTemplate(boxes_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}


/* unarchive a box */
function unarchiveBox(id) {
  $.get(url_api_v1_box_unarchive.replace(0, id), function(){
    var box_index = boxes_data.inactive_boxes.findIndex(function(element){
      return element.id == id;
    });
    boxes_data.active_boxes.push(boxes_data.inactive_boxes[box_index]);
    boxes_data.inactive_boxes.splice(box_index, 1);
    renderTemplate(boxes_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

$('#newBoxForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  var form_data = $('#newBoxForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    var box = {};
    response = response[0];

    box.id = response.pk;
    box.name = response.fields.name;
    box.url = url_view_box.replace(0, response.pk);
    boxes_data.active_boxes.push(box);
    renderTemplate(boxes_data);
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

$('#editBoxForm').on('submit', redirect);
function redirect(event) {
  event.preventDefault();
  var form_data = $('#editBoxForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    window.location.href = response.box;
  }, 'json')
    .fail(function(jqXHR) {
      if (jqXHR.status == 400 || jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: 'An error occurred while submitting the form.'});
      } else {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      }
    });
}
