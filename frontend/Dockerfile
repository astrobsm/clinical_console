# frontend/Dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY . /app
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost || exit 1
CMD ["nginx", "-g", "daemon off;"]
