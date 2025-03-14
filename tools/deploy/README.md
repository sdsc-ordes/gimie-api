# deployment manifests

## ytt

This directory contains kubernetes manifests templated with ytt.
The commands used to render and deploy these manifests are in [`manifests.just`](tools/just/manifests.just) and can be run using `just manifests`.

## How to use

To render these manifests in your own deployment repository, you could import them with [`vendir`](https://carvel.dev/vendir/) and render them with your [custom values](https://carvel.dev/ytt/docs/v0.51.0/ytt-data-values/).

