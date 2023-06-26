# Overview

This document provides a high-level architecture for the vision based order pickup solution.

## Problem statement

Create a vision-based order pickup solution which leverages ML on the edge capabilities in conjunction with Azure Applied AI Services to empower the retail store operations for improving the order pickup experience.

## User flow

The application is used in a flow where in a retain store such as a coffee shop or in a retail store a customer places an order waits for it to be prepared and collects it once ready.

The application focusses on the order pick-up flow specifically. Once the store operation personnel prepare the order, they place it in front of a camera connected to the hardware where our application is running.

The application will then process the information from the label and identifies the order information. Identified order information will then be called out using a computer-generated voice through a speaker.

![user journey](/docs/images/user-journey.jpg "User journey")

## Solution architecture

The Solution comprises of following 2 parts.

1.   Components that are deployed to every Store as Azure IoT Edge module, and

2.  A common set of components in Azure, that are shared across all the store deployed components.

![High level architectural diagram](/docs/images/architectural-diagram.jpg "Architectural Diagram")

## Solution Sequence

The solution has the following high-level components,

1. A **Video streaming** module deployed in store.

When the item containing the label is placed in front of a camera, the feed from the camera is converted into a Real Time Streaming Protocol (RTSP) stream by a component and passed over to "Edge inferencing" step.

*RTSP is a standard application-level network protocol for packetizing multimedia transport streams (video and audio). This step is useful to standardize the camera feed across various platform Mac/Windows/Linux*

2. An **Edge inferencing** deployed in store.

RTSP streams are passed on to an AI Model for Text detection. Once the Text is detected by the AI model, those video frames are passed onto next step for text extraction.

*Text detection done by the edge inferencing is useful to reduce the data flow between the store and the cloud components and thereby reducing the overall time and cost*

3. Azure Form Recognizer a SaaS solution deployed in the cloud as a **Text extraction** module

Azure form recognizer is a SaaS component running in Azure data center. The form recognizer will contain a pre-trained model to extract the relevant text from the sample images. When the edge component from the store provides an image to form recognizer, using the pre-trained model it will extract the relevant text from the image and responds back with a result object containing key-value pairs as defined in the model.

*Form recognizer needs to be re-trained when the format of the label changes. More information on training the form-recognizer model is here.*

4. A module that does **Label interpretation** of the extracted text deployed in the store.

The text response from Azure Form Recognizer contains keys and values as per trained model. The label interpretation module may receive multiple such responses for a video (multiple images will be sent to form recognizer) and has the intelligence to purge duplicates and identifies the order information. This module will then convert the order information that needs to be called out to an audio file using Azure TTS.

5. **A Web UI** that's connected with a speaker for the store operation personnel.

A Web UI will be running in a tablet/PC within the Store and this component will have a speaker attached to it. The Web UI contains a video loop of what's being captured by the camera. UI will receive the audio file through the WebSocket and will play it out through the speaker.

![Sequence flow diagram](/docs/images/sequence.jpg "Sequence flow diagram")

## Cross functional needs

### Observability

* Technical metrics from Edge components and cloud components are collected into Azure application insights for system monitoring.

* Business metrics like number of scans, latency and accuracy of the models are collected.

### Deployment

* Deployment of edge components are needed for every store. And configuration of cloud resources is needed for every label format.