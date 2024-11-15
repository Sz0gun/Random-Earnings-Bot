import os
import numpy as np
import pandas as pd
import tensorflow as tf
from binance.client import Client
from dotenv import load_dotenv
import time
import csv
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint, Callback, ReduceLROnPlateau, CSVLogger, TerminateOnNaN, BackupAndRestore
from ranger21 import Ranger21
from tensorflow.keras.optimizers import AdamW

load_dotenv()
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')


# Initialize Binance client
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)


# Define the function to fetch historical market data from Binance
def fetch_historical_data(symbol, interval, lookback):
    klines = client.get_historical_klines(symbol, interval, lookback)
    # Note: Using `pd.to_numeric()` with `errors='coerce'` allows us to convert the selected
    # columns to numeric types while automatically setting non-numeric values to `NaN`.
    # This helps prevent errors during processing if unexpected, non-numeric values are present in the data.


    columns = [
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close Time', 'Quote Asset Volume', 'Number of Trades',
        'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
    ]

    numeric_columns = [
        'Open', 'High', 'Low', 'Close', 'Volume',
        'Quote Asset Volume', 'Number of Trades',
        'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume'
    ]
    
    # Extract and convert klines into a DataFrame for easier processing
    data = pd.DataFrame(klines, columns=columns)

    # Convert numeric columns to appropriate types and keep only the relevant columns
    relevant_columns = [
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume'
    ]
    data = data[relevant_columns]
    data[
        ['Open', 'High', 'Low', 'Close', 'Volume']
    ] = data[
        ['Open', 'High', 'Low', 'Close', 'Volume']
    ].apply(pd.to_numeric, errors='coerce')
    return data

# Fetch historical data for Bitcoin
historical_data = fetch_historical_data("DOGEUSDT", Client.KLINE_INTERVAL_1HOUR, "90 days ago UTC")

# Prepare the data for training the model
def prepare_data(data, window_size=24):
    X = []
    y = []
    for i in range(len(data) - window_size):
        X.append(data['Close'].iloc[i:i+window_size].values)
        y.append(data['Close'].iloc[i+window_size])
    X, y = np.array(X), np.array(y)
    return X, y

X, y = prepare_data(historical_data)

# Split the data into training, validation, and test sets
train_size = int(0.7 * len(X))
val_size = int(0.15 * len(X))
X_train, X_val, X_test = X[:train_size], X[train_size:train_size + val_size], X[train_size + val_size:]
y_train, y_val, y_test = y[:train_size], y[train_size:train_size + val_size], y[train_size + val_size:]

# Define the LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1], 1)),
    tf.keras.layers.LSTM(50, return_sequences=True),
    tf.keras.layers.Dropout(0.2), # Added dropout to prevent overfitting
    tf.keras.layers.LSTM(50, return_sequences=False),
    tf.keras.layers.Dense(25),
    tf.keras.layers.Dropout(0.2), # One more
    tf.keras.layers.Dense(1)
])

# Compile the model

# Note: Mean Squared Error (MSE) is used as the loss function here. MSE gives greater weight to larger errors, which means the modell will focus more on minimizing large deviations.
# This is particularly useful in regression problems where larger errors are more costly.
# NRanger21 does not require a learning rate parameter in its default form, as it is internally managed for improved training stability.

adamw_opt = AdamW(learning_rate=0.001, weight_decay=1e-4)
model.compile(optimizer=adamw_opt, loss='mean_squared_error', metrics=['mae', 'mape'])
# ranger_opt = Ranger21(params=model.trainable_variables,lr=0.001)
# model.compile(optimizer=ranger_opt, loss='mean_squared_error', metric=['mae', 'mape'])


# Reshape the data for LSTM (add an additional dimension)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))


# Define Callbacks

# Note: EarlyStopping is used to stop training when there is no improvement in validation loss to avoid overfitting.

# Note: If `val_loss` stops improving but `train_loss` keeps decreasing, it indicates overfiting. Adjusting the model complexity or adding regularization techniques may be necessary.
# The 'patience' parameter defines how many without improvement in validation loss to wait before stopping the training. Increasing 'patience' allows the model to potentially overcome local minima.
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Note: TensorBoard is used to visualize the training process including metrics like loss, mae, and mape.
# Note: Monitor loss values over epochs - consistent decreases indicate good training. Sudden jumps may suggest learning rate issues.
tensorboard_callback = TensorBoard(log_dir='./logs/adamw', histogram_freq=1)

# Note: ReduceLROnPlateau decreases the learning rate when the validation process stop improving.
# Note: This helps in making finer adjustments to the model weights as training progresses, especially when convergence slows down.
# The `factor` parameter the rate by which the learning rate is reduced when no improvement in validation loss is detected.
# A value of 0.2 means the learning rate will be reduced to 20% if its current value, allowing finer adjustments.
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)

# Note: ModelCheckpoint saves the model after every epoch if there is an improvement in validation loss.
# Note: Saving the model ensures that the best version is retained. If `val_loss` improves significantly, it indicates good generalization; otherwise, consider early stopping or changing model arhitecture.
checkpoint_callback = ModelCheckpoint('model_checkpoint.keras', save_best_only=True, monitor='val_los', mode='min')

# Note: CSVLogger writes add training metrics to a CSV file after each epoch.
# Note: Keeping track of metrics over time is useful for post-training analysis and comparison between different models or training sessions.
csv_logger = CSVLogger('training_adamw.csv', append=True)

# Note: TerminateOnNaN stops the training process if the loss or any monitored metric becomes NaN.
# Note: This helps prevent wasting computational resources when the model encounters numerical instability.
terminate_on_nan = TerminateOnNaN()

# Note: BackupAndRestore creates checkpoints during training to resume in case of interuptions.
# Note: It is particularly useful for lengthy training processes where interruptions might result in significant loss of progress.
backup_restore = BackupAndRestore(backup_dir='./backup')

# Note: BatchLogger logs batch-level metrics to a CSV file for further analysis.
# Note: Monitoring batch-level metrics helps identify variations within batches and can point out issues like uneven data distribution.
class BatchLogger(Callback):
    def __init__(self, log_file='batch_logs.csv', threshold=0.05):
        self.log_file = log_file
        self.fieldnames = ['batch', 'loss', 'mae', 'mape']
        self.threshold = threshold
        self.batch_count = 0
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
        
    def on_batch_end(self, batch, logs=None):
        self.batch_count += 1
        # Log only if loss is above the defined threshold and every 10 batches
        if logs.get('loss') > self.threshold and self.batch_count % 10 == 0:
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                row = {field: logs.get(field) for field in self.fieldnames}
                row['batch'] = batch
                writer.writerow(row)

batch_logger = BatchLogger()

# Train the model with callbacks
# The batch size is redused to 16 to improve gradient stability during training.
# Smaller batch sizes can provide more detailes updates to model weights, which is particularly useful for preventing gradient explosion or vanishing.
model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    batch_size=16,
    epochs=50,
    callbacks=[
        early_stopping, tensorboard_callback, reduce_lr, checkpoint_callback,
        csv_logger, terminate_on_nan, backup_restore, batch_logger
    ]
)

# Save the trained model
model.save('adamw_model.keras')

