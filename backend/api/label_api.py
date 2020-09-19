
from flask import Blueprint, request, make_response

from model.project import Project
from mongoDBInterface import get_col

label_api = Blueprint('label_api', __name__)


#endpoint to add/delete/get preset labels
@label_api.route('/presetlabels', methods=['POST', 'GET', 'DELETE'])
def presetLabels():
    label_present = False
    #make sure project id is passed
    if 'projectName' in request.form:
        project_name = str(request.form['projectName'])
        labels_col = get_col(project_name, "labels")
        labels_cursor = labels_col.find({"name: <label>"})
        labels = list(labels_cursor)
        if (request.method == 'GET'):
            return labels
        #identify if passed label is already in the preset list
        if 'label' in request.form:
            label = request.json['label']
            project = Project(project_name, [], [])
            if label in labels:
                label_present = True
            if (request.method == 'POST'):
                if label_present:
                    response = {'status_code': 400, 'message':"Label already set"}
                else:
                    response = {'status_code': 200, 'message':"Added label successfully"}
                    labels.append(label)
                    project.set_labels(labels)
                response = make_response(response)
                return response
            if(request.method == 'DELETE'):
                if label_present:
                    labels.remove(label)
                    project.set_labels(labels)
                    response = {'status_code': 200, 'message': "Label deleted successfully"}
                else:
                    response = {'status_code': 400, 'message': "Label was not set"}
                response = make_response(response)
                return response
        else:
            response = {'status_code': 400,
                    'message': 'No label value provided'}
            response = make_response(response)
            return response
    else:
        response = {'status_code': 400,
                    'message': 'No project id provided'}
        response = make_response(response)
        return response
>>>>>>> 8647623... refactored latest merge
