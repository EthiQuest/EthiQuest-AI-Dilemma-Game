# Use an official Node runtime as the base image
FROM node:16

# Set the working directory in the container
WORKDIR /app
RUN npm cache clean --force

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the content of the local src directory to the working directory
COPY . .

# Build the app
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

# Specify the command to run on container start
CMD ["serve", "-s", "build", "-l", "3000"]