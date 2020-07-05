import face_alignment
from skimage import io

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)

input = io.imread('examples/Pictures2020/50_org_ref_Europaerinnen/98-04358_CF-0-1dummy0098_AGE_30_GLASSES_false_ETHNICITY_caucasian_TEINT_1.jpg')
preds = fa.get_landmarks(input)
print(preds)

