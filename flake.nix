{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;

          overlays = [
            (final: prev: {
              python = prev.python39;
            })
          ];
        };
      in {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.gnupg
            pkgs.git-cliff

            pkgs.python3
            pkgs.python39Packages.pip
            pkgs.pyright
            pkgs.litecli
            pkgs.pipreqs
            pkgs.python312Packages.nbconvert

            pkgs.chromedriver
            pkgs.selenium-manager
          ];
        };
      }
    );
}
