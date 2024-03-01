import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from collections import deque
import tkinter as tk
from threading import Thread
import time
import queue

# Define the asset
asset = 'GC=F'

# Get the live data
data = yf.download(tickers=asset, period="5d", interval="1m")

# Scale the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

# Create the training data
look_back = 60
x_train, y_train = [], []
for i in range(look_back, len(scaled_data)):
    x_train.append(scaled_data[i-look_back:i, 0])
    y_train.append(scaled_data[i, 0])
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Create the model
model = Sequential()
model.add(Dense(50, activation='relu', input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, epochs=50, batch_size=32, verbose=0)

# Initialize the portfolio
portfolio = {
    'cash': 100000,
    'shares': 0,
}

# Initialize the environment
env = {
    'data': data,
    'index': look_back,
    'portfolio': portfolio,
    'model': model,
    'scaler': scaler,
}

# Initialize the Q-table
Q_table = {}
for i in range(len(data) - look_back):
    for action in ['buy', 'sell']:
        Q_table[(i, action)] = 0

# Initialize the reward memory
reward_memory = deque(maxlen=100)

# Set the learning parameters
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
epsilon = 0.1  # exploration rate

def step(env, action):
    # Get the current data and portfolio
    data = env['data']
    portfolio = env['portfolio']
    model = env['model']
    scaler = env['scaler']

    # Get the current price
    price = data.loc[data.index[env['index']], 'Close']

    # Get the prediction
    prediction = model.predict(scaler.transform(data['Close'].values.reshape(-1, 1))[env['index']-look_back:env['index']].reshape(1, look_back, 1))
    prediction = prediction[0][0]

    # Calculate the confidence in the prediction
    confidence = abs(prediction - price) / price

    # Execute the action
    if (action == 'buy' and prediction > price) or (action == 'sell' and prediction < price):
        if action == 'buy':
            # Calculate the number of shares to buy based on the confidence
            shares = int(confidence * portfolio['cash'] / price)
            portfolio['cash'] -= shares * price
            portfolio['shares'] += shares
        elif action == 'sell':
            proceeds = portfolio['shares'] * price
            portfolio['cash'] += proceeds
            portfolio['shares'] = 0

    # Increment the index
    env['index'] += 1

    # Calculate the reward
    reward = portfolio['cash'] + portfolio['shares'] * price - 100000

    # Check if the prediction was correct
    correct = (prediction > price) == (data.loc[data.index[env['index']], 'Close'] > price)

    # Check if the simulation is done
    done = env['index'] >= len(data)

    return env, reward, done, correct

def run_trading_algorithm(message_queue):
    global env, reward_memory
    while True:
        # Choose an action
        if np.random.rand() < epsilon:
            action = np.random.choice(['buy', 'sell'])
        else:
            action = 'buy' if Q_table[(env['index'], 'buy')] > Q_table[(env['index'], 'sell')] else 'sell'

        # Step the environment
        env, reward, done, correct = step(env, action)

        # Update the Q-table
        old_state = (env['index'] - 1, action)
        new_state = (env['index'], 'buy' if correct else 'sell')
        Q_table[old_state] = (1 - alpha) * Q_table[old_state] + alpha * (reward + gamma * Q_table[new_state])

        # Add the reward to the reward memory
        reward_memory.append(reward)

        # Send a message to the GUI thread
        message_queue.put(f"Minute {env['index']}: Action = {action}, Correct = {correct}, Moving Average Reward = {np.mean(reward_memory)}\n")

        # Wait for a bit
        time.sleep(60)

        # Break if the simulation is done
        if done:
            break

# Create the GUI
gui = tk.Tk()
gui.title("Trading Algorithm")
gui.geometry("500x200")

# Create a text box for displaying the results
text_box = tk.Text(gui, width=50, height=10)
text_box.pack()

# Create a queue for communicating between threads
message_queue = queue.Queue()

# Create a function for updating the text box
def update_text():
    while True:
        # Check if there's a message in the queue
        if not message_queue.empty():
            # Get the message and insert it into the text box
            message = message_queue.get()
            text_box.insert(tk.END, message)
            text_box.see(tk.END)
        # Wait for a bit before checking again
        time.sleep(0.1)

# Create a thread for updating the GUI
gui_thread = Thread(target=update_text)
gui_thread.start()

# Start the trading algorithm on a separate thread
trading_thread = Thread(target=run_trading_algorithm, args=(message_queue,))
trading_thread.start()

# Run the GUI mainloop
gui.mainloop()
