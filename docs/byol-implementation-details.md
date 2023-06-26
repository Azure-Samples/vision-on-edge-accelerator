# Bring Your Own  Label

## Overview

The solution is shipped with a default Azure Form Recognizer custom neural model which has been trained on images of one specific type of beverage cup label in English. However, it supports a plug-in architecture where you can bring your own custom label or make changes to the label, train a custom model as per the new label and plug it in with the rest of the components using configurations and minimal to no code change. The configuration driven approach also allows you to pick and choose which of the fields extracted from the label you want displayed on the UI and/or narrated from the speaker.

## Steps

1. ### Choosing Between Custom Template and Neural Model

    A neural model is a deep learned model that combines layout and language features to extract fields from structured, semi-structured and unstructured documents. Whereas, a template model relies on a consistent visual template to extract fields from structured documents where the formatting and layout are static and constant.

    The default Azure Form Recognizer custom model in the solution has been trained using images collected randomly from the internet. Even though the layout of the beverage cup label is fixed across different stores and order types, the position of the label within the image is varying. For example, the label may be on the far left, right, top, bottom, rotated etc. The orientation of the cup across different images is also not the same, e.g. the cup is held in the hand at an angle or placed on a counter etc. Hence, the image of the beverage cup label is not considered a structured document in a strict sense in our use case.

    Considering this semi-structured nature of the document and better accuracy observed for this type of document during our initial experiments, we chose a custom neural model as a better choice for extracting fields from the beverage cup label.

    If your use case involves a structured document in a controlled environment (e.g. images taken in store environment from single type of camera device in a fixed area with the label always being placed upright in the center), we recommend evaluating a custom template model.

1. ### Create Azure Form Recognizer Custom Model

    Refer to the steps [here](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/how-to-guides/build-a-custom-model?view=form-recog-3.0.0&preserve-view=true#train-your-model) to create an Azure Form Recognizer custom model suited for your custom label.

1. ### Update Configurations

    Update the following configurations to make the solution work for your custom label:

    1. Narration Content  
        - Extracted fields from the label
        - Narration related properties such as voice, style, speech rate etc. Refer to [this](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup?tabs=csharp) link for more properties.
        - Narration content follows [string templates](https://docs.python.org/3/library/string.html#template-strings) in python. extracted information from the model can be used inside the `.tpl` files as template string.

        Sample configuration for narration content

        ```XML
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
            <voice name="en-US-SaraNeural">
                <express-as style="cheerful">
                    <prosody rate="10%" pitch="-5%">
                        Hello {name}
                        Your {item_name} is Ready
                    </prosody>
                </express-as>
            </voice>
        </speak>
        ```
