{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            (final: prev: {
              # Overlay to explicitly choose Python 3.9
              python = prev.python39;
            })
          ];
        };
      in
      {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.gnupg
            pkgs.git-cliff

            pkgs.python3 # Ensures Python 3.9 is installed
            pkgs.python39Packages.pip # Add pip
            pkgs.pyright 
            pkgs.litecli
            pkgs.pipreqs
          ];
        };
      }
    );
}
