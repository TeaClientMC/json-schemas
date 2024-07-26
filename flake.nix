{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv.url = "github:cachix/devenv";
  };

  outputs =
    inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.devenv.flakeModule ];
      systems = nixpkgs.lib.systems.flakeExposed;
      perSystem =
        {
          config,
          self',
          inputs',
          pkgs,
          system,
          ...
        }:
        {
          devenv.shells.default = {
            dotenv.enable = true;
            packages = with pkgs; [
              stdenv.cc.cc.lib # required by Jupyter
              (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
                python-lsp-server
                black
                mypy
                isort
              ]))
            ];
            languages.python = {
              enable = true;
              poetry = {
                enable = true;
                activate.enable = true;
                install.enable = true;
                install.allExtras = true;
              };
            };
          };
        };
    };
}
