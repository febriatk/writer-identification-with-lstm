# WRITER IDENTIFICATION USING LSTM

This project focuses on identifying authors based on handwriting patterns using the Long Short Term Memory (LSTM) algorithm. The study combines image processing techniques and deep learning to classify handwritten images into their respective writers. The model aims to learn distinctive handwriting characteristics and accurately distinguish between different authors.

## Dataset Information
- ### Source : Primary dataset collected for research purposes
- ### Description :
  - Handwritten images from 7 different writers
  - Each writer wrote 5 differents words, repeated 5 times
  - Total images : 175 samples
- ### Image Specification :
  - Image size : 50 x 50 pixels
  - File format : JPG
  - Black handwriting on white background
- ### Data Split :
  - Training data : 140 images
  - Testing data : 35 images

## Methodology
1. ### Image Preprocessing
   - Converted RGB images to grayscale using weighted conversion formula
   - Applied binary thresholding to obtain binary images
   - Resized images to 50 x 50 pixels
   - Converted image metrices into row vectors (2500 features)
   - Assigned labels and targets for supervised learning
   - Split dataset into training and testing set
3. ### Model Architecture
   The LSTM network architecture consist of :
   - Input Layer : 2500 units
   - Hidden Layer : 2500 units
   - Output Layer : 7 units (numbers of writers)
5. ### Model Training
   - Optimized using Backpropagation Through Time (BPTT)
   - Loss Function : Mean Squared Error (MSE)
   - Hyperparameter variations :
     - Learning rate : 0.009, 0.01, 0.015
     - Minimum error : 1 x 10^-5
     - Maximum epoch : 1000

## Results and Evaluation
- ### Training Results
  - Best accuracy achieved : 100%
  - Model successfully learned distintive handwriting patterns
  - Optimal convergence achieved with learning rate = 0.01
- ### Testing Results
  - Best learning rate : 0.015
  - Best error value : 1.96 x 10^-6
  - Best accuracy : 100%
The result indicate that the LSTM model is capable of capturing sequential and structural patterns in handwritten images and effectively distinguishing between different authors.

## Conclusion
This project demonstrates that image preprocessing combined with LSTM neural networks can effectively solve the problem of writer identification based on handwriting patterns. The model achieved high accuracy on both training and testing data, indicating strong pattern recognition capability.

Future improvements may include :
- Expanding the dataset with more writers
- Applying cross-validation for robustness
- Comparing LSTM performance with CNN-based architectures
