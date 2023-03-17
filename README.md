# autrum

This project porpoise is to stream and visualize real-time audio data in time and frequency domains. It uses the scipy library to capture audio from the user's microphone, processes the data, and displays the results using matplotlib.

## Installation

To install the dependencies for this project, run the following command:

```
pip install -r requirements.txt
```

## Usage

To run the project, run the main.py script:

```
python main.py
```

This will initialize the UI that has two graphs, one for time domain and one for the frequency one. You can use the toolbar beneath the graphs to perform functions like zoom-in zoom-out

![Toolbar](doc/toolbar.png "Graphs Toolbar")

The UI has three main buttons, record audio, open saved atm files, and playback those files:

![Buttons](doc/buttons.png "Action Buttons")

The play button will be disabled until a file is selected

This is how the app looks:
![Home](doc/home.png "Home")

## Know problems

- When replaying saved atm files, the graphs will be drawn instantly, not in real-time how its expected. The cause of the problem, audio thread was having problems updating the canvas (which was on the main thread); also, performance issues.
- When recording audio the user can't pause and resume the recording, it has to stop the recording and start a new one.

## Why are the members' voices different?

Some physical characteristics of the vocal cords like length, thickness, and tension have impact on the frequency result of them speaking, causing this difference. The medium in which the voice is propagated also can affect the result.
