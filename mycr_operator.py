import kopf
import logging
from kubernetes import client, config

# Load Kubernetes configuration from default location
config.load_kube_config()

@kopf.on.create('example.com', 'v1', 'mycrds')
def handle_create(body, **kwargs):
    # Extract inputs from the custom resource
    spec = body.get('spec', {})
    volumes = spec.get('volumes', [])

    # Create a Kubernetes resource based on the inputs
    for volume in volumes:
        name = volume.get('name')
        size = volume.get('size')

        # Create a PVC resource
        api = client.CoreV1Api()
        pvc_manifest = {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "name": f"pvc-{name}"
            },
            "spec": {
                "accessModes": ["ReadWriteOnce"],
                "resources": {
                    "requests": {
                        "storage": size
                    }
                }
            }
        }
        api.create_namespaced_persistent_volume_claim(namespace="default", body=pvc_manifest)
        print(f"PVC created: pvc-{name} with size {size}")

if __name__ == "__main__":
    kopf.run(namespace="default")

