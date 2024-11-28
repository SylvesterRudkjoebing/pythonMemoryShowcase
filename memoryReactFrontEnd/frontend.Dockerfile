# Use an official Node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend application
COPY . .

# Build the app
RUN npm run build

# Install serve to run the build
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Run the app
CMD ["serve", "-s", "build", "-l", "3000"]