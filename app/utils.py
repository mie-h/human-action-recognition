import albumentations as A

# define the transforms
transform = A.Compose(
    [
        # resize the image to 128×171 dimension which is in regard to the training dimensions
        A.Resize(128, 171, always_apply=True),
        # apply center cropping to the frames to crop them to 112×112 dimensions
        A.CenterCrop(112, 112, always_apply=True),
        # All pre-trained models expect input images normalized in the same way
        A.Normalize(
            mean=[0.43216, 0.394666, 0.37645],
            std=[0.22803, 0.22145, 0.216989],
            always_apply=True,
        ),
    ]
)
# read the class names from labels.txt
with open("labels.txt", "r") as f:
    class_names = f.readlines()
    f.close()
