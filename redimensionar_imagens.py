from pathlib import Path
import argparse

from PIL import Image, ImageOps


def redimensionar_imagens(input_dir: Path, largura: int, altura: int, output_dir: Path | None, sobrescrever: bool) -> tuple[int, int, int]:
    suportadas = {".png", ".jpg", ".jpeg", ".webp"}
    processadas = 0
    ignoradas = 0
    sem_alteracao = 0

    if not input_dir.exists() or not input_dir.is_dir():
        raise ValueError(f"Pasta de entrada invalida: {input_dir}")

    destino_base = input_dir if sobrescrever else (output_dir or (input_dir / "redimensionadas"))
    destino_base.mkdir(parents=True, exist_ok=True)

    for arquivo in sorted(input_dir.iterdir()):
        if not arquivo.is_file() or arquivo.suffix.lower() not in suportadas:
            ignoradas += 1
            continue

        try:
            with Image.open(arquivo) as img:
                if img.size == (largura, altura):
                    sem_alteracao += 1
                    continue

                # Mantem proporcao sem corte e centraliza com bordas no tamanho final.
                base = ImageOps.contain(img.convert("RGBA"), (largura, altura), method=Image.Resampling.LANCZOS)
                if arquivo.suffix.lower() in {".jpg", ".jpeg"}:
                    capa = Image.new("RGB", (largura, altura), (255, 255, 255))
                    offset = ((largura - base.width) // 2, (altura - base.height) // 2)
                    capa.paste(base.convert("RGB"), offset)
                else:
                    capa = Image.new("RGBA", (largura, altura), (255, 255, 255, 0))
                    offset = ((largura - base.width) // 2, (altura - base.height) // 2)
                    capa.paste(base, offset, base)

                if sobrescrever:
                    destino = arquivo
                else:
                    destino = destino_base / arquivo.name

                if arquivo.suffix.lower() == ".png":
                    capa.save(destino, format="PNG", optimize=True)
                elif arquivo.suffix.lower() in {".jpg", ".jpeg"}:
                    capa.save(destino, format="JPEG", quality=95, optimize=True)
                else:
                    capa.save(destino)

                processadas += 1
        except Exception as exc:
            ignoradas += 1
            print(f"Falha ao processar {arquivo.name}: {exc}")

    return processadas, ignoradas, sem_alteracao


def main() -> None:
    base_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="Redimensiona imagens para 268x402 (largura x altura)."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=base_dir / "static/images",
        help="Pasta com as imagens de entrada (padrao: static/images).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Pasta de saida. Se omitido, usa static/images/redimensionadas (ou sobrescreve com --sobrescrever).",
    )
    parser.add_argument(
        "--largura",
        type=int,
        default=268,
        help="Largura final em pixels (padrao: 268).",
    )
    parser.add_argument(
        "--altura",
        type=int,
        default=402,
        help="Altura final em pixels (padrao: 402).",
    )
    parser.add_argument(
        "--sobrescrever",
        action="store_true",
        help="Sobrescreve os arquivos originais em static/images.",
    )

    args = parser.parse_args()

    input_dir = args.input_dir if args.input_dir.is_absolute() else (base_dir / args.input_dir)
    output_dir = None
    if args.output_dir is not None:
        output_dir = args.output_dir if args.output_dir.is_absolute() else (base_dir / args.output_dir)

    processadas, ignoradas, sem_alteracao = redimensionar_imagens(
        input_dir=input_dir,
        largura=args.largura,
        altura=args.altura,
        output_dir=output_dir,
        sobrescrever=args.sobrescrever,
    )

    print(f"Processadas: {processadas}")
    print(f"Ignoradas: {ignoradas}")
    print(f"Sem alteracao (ja estavam em {args.largura}x{args.altura}): {sem_alteracao}")
    if not args.sobrescrever:
        destino = output_dir or (input_dir / "redimensionadas")
        print(f"Imagens salvas em: {destino}")


if __name__ == "__main__":
    main()
