import tensorflow as tf
from tensorflow import keras
from keras import layers, models
from keras.preprocessing.image import ImageDataGenerator

# Step 1: Define the image size and batch size
image_size = (64, 64)  # Correct image size
batch_size = 32

# Step 2: Create the ImageDataGenerator and load the data with data augmentation
datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,     # Randomly rotate images by 20 degrees
    width_shift_range=0.2,  # Randomly shift images horizontally by 20% of the width
    height_shift_range=0.2,  # Randomly shift images vertically by 20% of the height
    zoom_range=0.2,        # Randomly zoom in by 20%
    horizontal_flip=True,  # Randomly flip images horizontally
)
train_generator = datagen.flow_from_directory(
    'shapes',  # Correct path to the dataset folder
    target_size=image_size,
    batch_size=batch_size,
    class_mode='sparse'  # Use 'sparse' for integer labels
)

# Step 3: Create the model architecture
num_classes = 3  # Replace 10 with the number of classes in your dataset
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),  # Add dropout to reduce overfitting
    layers.Dense(num_classes, activation='softmax')
])

# Step 4: Compile the model with a lower learning rate
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])

# Step 5: Train the model using the data generator
epochs = 100
model.fit(train_generator, epochs=epochs)

# Step 6: Save the model for future use
model.save('my_image_classifier.keras')

print("Done")
