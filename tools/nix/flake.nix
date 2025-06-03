{
  description = "gimie-api";

  inputs = {
    # Nixpkgs
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    # You can access packages and modules from different nixpkgs revs
    # at the same time. Here's an working example:
    nixpkgsStable.url = "github:nixos/nixpkgs/nixos-23.11";
    # Also see the 'stable-packages' overlay at 'overlays/default.nix'.

    flake-utils.url = "github:numtide/flake-utils";

  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    let
      # The function which builds the flake output attrMap.
      defineOutput =
        system:
        let
          # inherit from nixpkgs
          pkgs = nixpkgs.legacyPackages.${system};

          # Things needed only at compile-time.
          packagesBasic = with pkgs; [
            age
            bash
            coreutils
            curl
            findutils
            git
            imgpkg
            just
            kubectl
            sops
            uv
            vendir
            yamlfmt
            ytt
            zsh
          ];

        in
        {
          devShells = {
            default = pkgs.mkShell {
              packages = packagesBasic;
            };
          };
        };
    in
    # Creates an attribute map `{ <key>.<system>.default = ...}`
    # by calling function `defineOutput`.
    # Key sofar is only `devShells` but can be any output `key` for a flake.
    flake-utils.lib.eachDefaultSystem defineOutput;
}
