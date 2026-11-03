{
  description = "Flappy dev shell with pygbag";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.python312 pkgs.git pkgs.ffmpeg ];
        shellHook = ''
          if [ ! -d .venv ]; then
            python -m venv .venv
          fi
          source .venv/bin/activate
          pip install --quiet pygbag pygame-ce
        '';
      };
    };
}
