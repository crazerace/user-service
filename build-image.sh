CONTAINER_REGISTRY=$(cat package.json | jq .repository --raw-output)
IMAGE_NAME=$(cat package.json | jq .name --raw-output)
IMAGE_VERSION=$(cat package.json | jq .version --raw-output)
IMAGE_NAME="$CONTAINER_REGISTRY/$IMAGE_NAME:$IMAGE_VERSION"

docker build -t $IMAGE_NAME .