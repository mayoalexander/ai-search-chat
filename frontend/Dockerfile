# Use official Node.js slim image
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

## No build step needed for dev server

# Expose port
EXPOSE 3000

# Start the Next.js dev server for hot reloading
CMD ["npm", "run", "dev"]