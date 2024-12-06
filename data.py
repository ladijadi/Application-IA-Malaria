import tensorflow as tf
import tensorflow_datasets as tfds

# Charger le dataset
dataset, info = tfds.load("malaria", as_supervised=True, with_info=True)

# Taille cible des images
TARGET_SIZE = (128, 128)

# Fonction pour redimensionner les images
def preprocess_image(image, label):
    image = tf.image.resize(image, TARGET_SIZE)  # Redimensionner l'image
    image = tf.cast(image, tf.float32) / 255.0   # Normaliser les pixels à [0, 1]
    return image, label

# Prétraiter le dataset
train = dataset['train'].take(int(0.7 * info.splits['train'].num_examples))
val = dataset['train'].skip(int(0.7 * info.splits['train'].num_examples)).take(int(0.15 * info.splits['train'].num_examples))
test = dataset['train'].skip(int(0.85 * info.splits['train'].num_examples))

train = train.map(preprocess_image).batch(32).prefetch(tf.data.AUTOTUNE)
val = val.map(preprocess_image).batch(32).prefetch(tf.data.AUTOTUNE)
test = test.map(preprocess_image).batch(32).prefetch(tf.data.AUTOTUNE)

# Vérification des tailles
print(f"Train size: {tf.data.experimental.cardinality(train).numpy()}")
print(f"Validation size: {tf.data.experimental.cardinality(val).numpy()}")
print(f"Test size: {tf.data.experimental.cardinality(test).numpy()}")