# **HAND GESTURE - BASED MEDIA CONTROL SYSTEM**
---
## **PROJECT GOAL:**
The primary goal of your project is to enable users to control media playback (e.g., playing, pausing, adjusting volume, navigating) using hand gestures, offering a hands-free and intuitive way to interact with devices.
## **IMPLEMENTATION:**
* A dataset of hand gesture images is created.
* A convolutional neural network (CNN) model (MobileNetV2) is trained to recognize the different hand gestures.
* This mainly uses transfer learning. The model being used is MobileNetV2, which is a pre-trained model. This means it has been previously trained on a large dataset (ImageNet) to recognize a wide variety of objects.
* The trained model is integrated into a Streamlit application. The application captures video frames from a webcam. The ROI is extracted from each frame. The trained model predicts the hand gesture present in the ROI.
* Based on the predicted gesture, the application uses the pyautogui library to simulate keyboard key presses, which control the media player.
## **APPLICATIONS:**
1. Accessibility Support: Assists users with physical disabilities in controlling media players without the need for physical contact.
2. Smart Home Systems: Integrates with smart TVs and multimedia devices for intuitive control using simple gestures.
3. Public Displays and Kiosks: Provides touchless interaction with digital displays in public spaces, reducing the spread of germs.
4. Gaming and VR/AR Systems: Enhances immersive experiences by enabling natural hand movements to control media or navigate interfaces.
---

**Dataset taken from:** https://www.kaggle.com/datasets/barnabaspeter/hand-gesture-dataset

**View my Project at:**  
