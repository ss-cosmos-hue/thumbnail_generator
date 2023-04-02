import json
import requests


# Returns relative y-coord for bottom of face, and confidence in face-detection accuracy
def bottom_detector(image_path):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmYzODY4MTctMDlmYy00NjBlLTljOWItMjQ2ZGYzYmE0NzliIiwidHlwZSI6ImFwaV90b2tlbiJ9.WOwzUmc3IkbtDxHSrUiLdTYE7wZS2COY5vC8hsmX3_A"}

    url = "https://api.edenai.run/v2/image/face_detection"
    data = {"providers": "clarifai"}
    files = {'file': open(image_path, 'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)

    face_bottoms = []
    face_confidence = []
    # Print info for each face
    i = 0
    # Loop for number of faces in result['clarifai']['items']
    for item in (result['clarifai']['items']):
        # Add current face bottom to list
        face_bottoms.append(result['clarifai']['items']
                            [i]['bounding_box']['y_max'])
        # Add current face confidence to list
        face_confidence.append(result['clarifai']['items'][i]['confidence'])
        i += 1  # Iterate to new face

    face_data = [face_bottoms, face_confidence]
    return face_data[:]


def bottom_value_decider(image_path):
    # Call bottom detector to return 2 lists of -- 1) "y_max"'s and 2) confidence levels -- in a list
    face_result = bottom_detector(image_path)
    # print(face_result)
    face_count = len(face_result[0])  # Assign number of faces to a variable
    # Bottom value is the applicable 'y_max' # Assigned to such a random number so that detection of no change is trackable
    bottom_value = -3249429594509234095243095
    scaleable_faces = []  # List of bottom values in case we have multiple scalable faces
    if (face_count == 1):  # Check if number of faces is 1 (simplest case)
        if (face_result[1][0] > .8):  # Check if confidence in face is > 80%
            # If so, set the y_max of that face to the bottom value
            bottom_value = face_result[0][0]
    elif (face_count > 1):  # Check if number of faces is more than 1 (more complex case)
        i = 0  # Set up our while loop
        while (i < face_count):  # Iterate for every single face
            if (face_result[1][i] > .8):  # Check if confidence in this face is > 80%
                # If so, add y_max of that face to list of scalable faces
                scaleable_faces.append(face_result[0][i])
            i += 1  # Increment to next face
        if (len(scaleable_faces) > 1):  # Check if number of scalable faces is > 1 (more complex case)
            # If so, set first scalable face to the bottom value by default
            bottom_value = scaleable_faces[0]
            # Check each bottom value after the first to see which is greatest
            for i in range((len(scaleable_faces))):
                # Check is face's y_max is greater than others
                if scaleable_faces[i] >= bottom_value:
                    # If so, set that face's y_max to new bottom_value
                    bottom_value = scaleable_faces[i]
        else:  # Else if number of scalable faces is 0 (simplest case)
            # Set bottom value equal to only scalable face
            bottom_value = scaleable_faces[0]
    # Return bottom value to be used as relative lowest point on face
    return(bottom_value)

# print(bottom_value_decider("mario.png"))
