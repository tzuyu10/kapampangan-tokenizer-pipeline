"""Build two matched Kaggle training notebooks and their exact private inputs.

Reuse the user-supplied penalty32 notebook's cells with checked substitutions.
Copy authoritative candidate tokenizers; never reconstruct their IDs or merges.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import textwrap
import zipfile

from training_support import read_matched_csv, validate_variant_artifact, variant_fields


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DESTINATION = ROOT / "release-assets/infix_first_training"
TEMPLATE = ROOT / "notebooks/NLLB_600M_Penalty32_Source_Embedding_Training.ipynb"
TEMPLATE_SHA = "f581ad2695124de8d254348be30075e39216046c19924a7e2c60dedf771ee315"
EXPECTED_DATA = "69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b"
DEFAULT_ARTIFACT_ROOT = Path("C:/Users/Gabo/.codex/visualizations/2026/10/10/01a123b1-9446-7a33-b574-09074e63c7e7/infix_penalty_comparison")
VARIANTS = {
    16: "bcca72bb94b2bf356ec763414670f1b06306284d71ea46ee07119da34ebdeb2c",
    48: "fb606893cca542488118853aa58a5d97ebd7c02e51a1bdd9c54af09dc3625e86",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def write_zip(path, files):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(files):
            raise ValueError("Generated ZIP failed integrity checking")
        for name, content in files.items():
            if archive.read(name) != content:
                raise ValueError("Generated ZIP changed bytes: " + name)
    return sha(path.read_bytes())


def substitute(source, old, new):
    if old not in source:
        raise ValueError("Template anchor changed: " + old[:100])
    return source.replace(old, new)


def text_cell(source, code=False):
    result = dict(cell_type="code" if code else "markdown", metadata={},
                  source=textwrap.dedent(source).strip() + "\n")
    if code:
        result.update(execution_count=None, outputs=[])
    return result


def make_notebook(penalty, package_sha, manifest_sha, reference):
    if sha(TEMPLATE.read_bytes()) != TEMPLATE_SHA:
        raise ValueError("The supplied penalty32 template changed; review before regenerating")
    notebook = copy.deepcopy(json.loads(TEMPLATE.read_text(encoding="utf-8")))
    variant = f"infix_first_penalty{penalty}"
    notebook_name = f"NLLB_600M_InfixFirst_Penalty{penalty}_Source_Embedding_Training.ipynb"
    for cell in notebook["cells"]:
        source = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        source = source.replace("weighted_penalty32", variant).replace("penalty32", variant)
        source = source.replace("Penalty-32 Morph-BPE", f"Infix-first penalty-{penalty} Morph-BPE")
        source = source.replace("penalty-32", f"infix-first penalty-{penalty}")
        source = source.replace("crossing_penalty=32", f"crossing_penalty={penalty}")
        source = source.replace("['crossing_penalty'] != 32", f"['crossing_penalty'] != {penalty}")
        cell["source"] = source
        if cell["cell_type"] == "code":
            cell.update(execution_count=None, outputs=[])
    cells = notebook["cells"]
    cells[0] = text_cell(f"""
        # Infix-first penalty {penalty}: NLLB source-embedding training

        Train a **new 6,080 x 1,024 source embedding table** for the actual infix-first
        penalty-{penalty} tokenizer. Its first phase prioritizes recognized infixes;
        the remaining vocabulary uses weighted morphology-aware BPE. There is no
        additional root-first phase. The tokenizer is already trained and packaged.
        The penalty changes its learned merge rules, not the translation loss.

        All pretrained NLLB encoder layers, decoder, native Filipino target embeddings
        and output projection stay frozen. Each candidate starts independently from
        the same pinned NLLB base. Token IDs and embeddings from current32 or the other
        candidate are incompatible and cannot be reused.

        Matched recipe: seed42, native-subtoken warm initialization, learning rate
        0.0003, batch1, accumulation8, maximum30 epochs, early stopping patience3 and
        minimum improvement0.001. Source/target limits remain256/128. Selection uses
        lowest validation loss, and saved history reports actual completed epochs.

        Upload `infix_first_penalty{penalty}_training_inputs.zip` as a private Kaggle
        dataset. It includes the exact matched CSV, tokenizer/runtime, native target
        tokenizer, unchanged training helper and baseline provenance. It contains no
        trained source weights. Enable GPU and Internet for dependencies and the
        pinned base download. ZIP and automatically expanded inputs are supported.

        Optional `current_weighted32_reference.zip` evaluates the currently installed
        weighted32 model with the same rows and FP32 decoding. It is an inference
        reference and is never used for initialization or resume. Run cells in order.
        Both translation-evaluation switches default to False. The original notebook
        and installed models are preserved. Local preparation did not run GPU training.
        """)
    cfg = cells[4]["source"]
    cfg = cfg.replace(f"{variant}_warm_start_seed42_v2", f"{variant}_warm_start_seed42_v1")
    cfg = substitute(cfg, "RUN_TEST = False", "RUN_CURRENT32_REFERENCE = False\nCURRENT32_REFERENCE_PATH = ''\nRUN_TEST = False")
    cfg = re.sub(r"EXPECTED_PACKAGE_SHA256 = '[a-f0-9]+'", f"EXPECTED_PACKAGE_SHA256 = '{package_sha}'", cfg)
    cfg = re.sub(r"EXPECTED_PACKAGE_MANIFEST_SHA256 = '[a-f0-9]+'", f"EXPECTED_PACKAGE_MANIFEST_SHA256 = '{manifest_sha}'", cfg)
    cfg = re.sub(r"EXPECTED_TOKENIZER_FINGERPRINT = '[a-f0-9]+'", f"EXPECTED_TOKENIZER_FINGERPRINT = '{VARIANTS[penalty]}'", cfg)
    cfg = substitute(cfg, "PLATFORM = ", f"PENALTY = {penalty}\nVARIANT = '{variant}'\nEXPECTED_REFERENCE_SHA256 = '{reference['zip_sha256']}'\nEXPECTED_REFERENCE_MANIFEST_SHA256 = '{reference['manifest_sha256']}'\nPLATFORM = ")
    cells[4]["source"] = cfg
    cells[3] = text_cell(f"""
        ## 2. Choose inputs and a new output run

        Blank paths discover the matching Kaggle ZIP or expanded package. The notebook
        distinguishes penalty16 and48 even when both are attached. Use `RESUME=False`
        for a fresh run. Resume requires this exact candidate's full backup including
        `last.pt`; current32, Plain BPE, the other penalty and inference-only ZIPs are
        rejected. `RUN_NAME` must be a single folder name.

        Kaggle working storage belongs to the session. Save/download outputs before
        ending it. Checkpoints are saved at completed-epoch boundaries; an interrupted
        epoch repeats when resumed. For the first run, keep all evaluation switches
        False. Set `RUN_VALIDATION_TRANSLATIONS=True` to compare validation outputs.
        Set `RUN_TEST=True` for final scoring after freezing the experiment settings.
        Add the reference ZIP and enable `RUN_CURRENT32_REFERENCE` for a matched
        current32 comparison. Refer to the included README for the full workflow.
        """)
    verify = cells[6]["source"]
    verify = substitute(verify, f".get('package_kind') == '{variant}_source_training'",
                        ".get('package_kind') == 'infix_first_source_training'\n                      and json.loads(p.read_text()).get('tokenizer_variant') == VARIANT\n                      and json.loads(p.read_text()).get('crossing_penalty') == PENALTY")
    verify = substitute(verify, f"if package['package_kind'] != '{variant}_source_training':",
                        "if (package['package_kind'] != 'infix_first_source_training' or\n    package['tokenizer_variant'] != VARIANT or package['crossing_penalty'] != PENALTY):")
    start = verify.index("if artifact_manifest['actual_vocabulary_size']")
    end = verify.index("for line in (ARTIFACT/'checksums.sha256')", start)
    verify = verify[:start] + textwrap.dedent("""
        sys.path.insert(0, str(INPUT_ROOT))
        from training_support import (variant_fields, validate_variant_artifact,
            validate_saved_manifest, validate_runtime_files, validate_checkpoint,
            validate_best_weights, identity_digest, reload_report_matches, extract_safe_zip)
        VARIANT_FIELDS = validate_variant_artifact(artifact_manifest,
            json.loads((ARTIFACT/'tokenizer.json').read_text()), PENALTY, EXPECTED_TOKENIZER_FINGERPRINT)
        if package.get('trained_source_weights_included') is not False:
            raise ValueError('Training inputs must not contain trained source weights')
        """).lstrip() + verify[end:]
    verify = verify.replace("Wrong weighted tokenizer configuration", "Wrong infix-first tokenizer configuration")
    cells[6]["source"] = verify
    run = cells[12]["source"]
    run = substitute(run, "identity.update(condition='morph_bpe',", "identity.update(**VARIANT_FIELDS)\nidentity.update(condition='morph_bpe',")
    run = substitute(run, "runtime_controls=RUNTIME_CONTROLS,", "runtime_controls=RUNTIME_CONTROLS,\n                tokenizer_fingerprint=EXPECTED_TOKENIZER_FINGERPRINT,\n                input_package_manifest_sha256=EXPECTED_PACKAGE_MANIFEST_SHA256,\n                target_tokenizer_sha256=digest(INPUT_ROOT/'target_tokenizer/tokenizer.json'),\n                evaluation_support_sha256=digest(INPUT_ROOT/'evaluation_support.py'),")
    # Validate imported full backups before accepting files into the selected run.
    start = run.index("            with zipfile.ZipFile(resume_path) as archive:")
    end = run.index("            info = json.loads", start)
    run = run[:start] + "            extract_safe_zip(resume_path, temp)\n" + run[end:]
    run = substitute(run, "            if info['identity'] != identity or info['cfg'] != CFG:\n                raise ValueError('Not this exact " + variant + " run/configuration')",
                        "            validate_saved_manifest(info, identity, CFG)\n            validate_runtime_files(temp, identity)")
    run = substitute(run, "        if info['identity'] != identity or info['cfg'] != CFG:\n            raise ValueError('Not this exact " + variant + " run/configuration')",
                        "        validate_saved_manifest(info, identity, CFG)\n        validate_runtime_files(resume_path, identity)")
    start = run.index("    if saved['identity'] != identity")
    end = run.index("    del saved, saved_best", start)
    run = run[:start] + textwrap.indent(textwrap.dedent("""
        validate_saved_manifest(json.loads((OUT/'manifest.json').read_text()), identity, CFG)
        validate_runtime_files(OUT, identity)
        validate_checkpoint(saved, identity, CFG, lambda tensor: torch.isfinite(tensor).all())
        from safetensors.torch import load_file
        saved_best = load_file(str(OUT/'best_source.safetensors'))['weight']
        validate_best_weights(saved_best, lambda tensor: torch.isfinite(tensor).all())
        """).lstrip(), "    ").rstrip() + "\n" + run[end:]
    run = substitute(run, "for name in ['source_artifact', 'runtime', 'target_tokenizer']:",
                        "manifest.update(**VARIANT_FIELDS)\nfor name in ['source_artifact', 'runtime', 'target_tokenizer']:")
    run = substitute(run, "shutil.copy2(INPUT_ROOT/'training_support.py', OUT/'training_support.py')",
                        "shutil.copy2(INPUT_ROOT/'training_support.py', OUT/'training_support.py')\nshutil.copy2(INPUT_ROOT/'evaluation_support.py', OUT/'evaluation_support.py')")
    run = substitute(run, "helper.save_json(OUT/'split_manifest.json', {k:[r['id'] for r in v] for k,v in splits.items()})",
                        "shutil.copy2(INPUT_ROOT/'reference/plain_bpe/split_manifest.json', OUT/'split_manifest.json')\nvalidate_runtime_files(OUT, identity)")
    cells[12]["source"] = run
    cells[11] = text_cell("""
        ## 6. Prepare a separate run or verify an exact resume

        Identity includes the actual infix-first algorithm, penalty, artifact, runtime,
        helper, support modules, native target tokenizer, data, ordered splits and
        configuration. A fresh run refuses existing weights. Application routing is
        `morph_bpe`; research variant is recorded separately and cannot be confused
        with current weighted32. No trained checkpoint supplies fresh initialization.
        """)
    reload = cells[18]["source"]
    start = reload.index("    if reload_info['identity'] != identity")
    end = reload.index("    from safetensors.torch", start)
    reload = reload[:start] + "    validate_saved_manifest(reload_info, identity, CFG)\n    validate_runtime_files(OUT, identity)\n" + reload[end:]
    reload = substitute(reload, "reload_report = dict(status='passed',", "reload_report = dict(**VARIANT_FIELDS, identity_sha256=identity_digest(identity), status='passed',")
    cells[18]["source"] = reload
    cells[19] = text_cell("""
        ## 9. Optional candidate translation evaluation

        Validation evaluation supports decisions. Keep final test scoring until both
        candidate recipes are frozen. FP32 generation uses four beams and160 new
        tokens, raw CSV references, BLEU13a and chrF++ with word order2. Progress
        resumes only with the same weights, tokenizer, row order, settings and versions.
        Outputs include predictions, scores, metric signatures and output-limit counts.
        Loss is the training objective; BLEU/chrF++ are measured after training.
        """)
    cells[20] = text_cell("""
        from evaluation_support import evaluate_selected, verify_reference, compare_scores
        if digest(INPUT_ROOT/'evaluation_support.py') != identity['evaluation_support_sha256']:
            raise ValueError('Evaluation implementation changed')
        eval_splits = ([] if not RUN_VALIDATION_TRANSLATIONS else ['validation']) + ([] if not RUN_TEST else ['test'])
        for split in eval_splits:
            evaluate_selected(model, source, target, splits[split], split, OUT/'evaluation'/split,
                              OUT, EXPECTED_DATA_SHA256, DEVICE, BEAMS, MAX_NEW_TOKENS, SOURCE_LIMIT)
        if not eval_splits:
            print('Translation scoring skipped. Enable a switch and rerun after completed training.')
        """, code=True)
    cells[21] = text_cell("""
        ## 10. Export inference and full resume backups

        The inference ZIP has `manifest.json` at its root and excludes optimizer state.
        It cannot resume training. Keep the full ZIP for an epoch-boundary resume. Both
        contain the candidate's source tokenizer, native target tokenizer and helpers;
        the frozen NLLB base is downloaded separately. Completed inference export
        requires a passing saved-bundle reload check bound to these exact weights,
        identity, selected epoch and decoding settings. An interrupted run can export
        a full backup after at least one completed epoch.

        Training creates separate files. Evaluate the candidates before deciding
        whether to install one in the application. Installation is a separate step.
        """)
    export = cells[22]["source"]
    start = export.index("for name,key in")
    end = export.index("FULL_ZIP = ", start)
    export = export[:start] + "validate_saved_manifest(info, identity, CFG)\nvalidate_runtime_files(OUT, identity)\n" + export[end:]
    start = export.index("    reload_ok = (report.get('status')")
    end = export.index("if info.get('training_status')", start)
    export = export[:start] + "    reload_ok = reload_report_matches(report, info, OUT)\n" + export[end:]
    # Include matched reference evaluation inside candidate exports, not its weights.
    export = substitute(export, "FULL_ZIP = Path(", "reference_scores = WORK/'reference_evaluation'/'weighted_penalty32'\nif reference_scores.exists():\n    shutil.copytree(reference_scores, OUT/'evaluation'/'current_weighted32_reference', dirs_exist_ok=True)\nFULL_ZIP = Path(")
    cells[22]["source"] = export
    cells[21:21] = [text_cell("""
        ### 9.1 Optional matched comparison against current weighted32

        Attach the reference ZIP and enable `RUN_CURRENT32_REFERENCE`. This scores
        current32 on the same enabled partitions, using its own source embeddings
        and tokenizer. The candidate GPU model is released before loading current32.
        The CSV reports candidate-minus-current32 BLEU/chrF++; positive values mean
        higher corpus scores. Differences alone do not establish significance.

        To rerun candidate scoring afterward, rerun section8.1 to reload its bundle.
        """), text_cell("""
        if RUN_CURRENT32_REFERENCE:
            if not eval_splits:
                raise ValueError('Enable validation or final test scoring before current32 comparison')
            reference_bundle, reference_info = verify_reference(
                CURRENT32_REFERENCE_PATH, SEARCH_ROOTS, WORK,
                EXPECTED_REFERENCE_SHA256, EXPECTED_REFERENCE_MANIFEST_SHA256,
                EXPECTED_DATA_SHA256, REVISION, identity['helper_sha256'],
                identity['target_tokenizer_sha256'], CFG, baseline_splits)
            if 'model' in globals():
                del model
            import gc
            gc.collect(); torch.cuda.empty_cache()
            # Import the baseline's runtime from its verified files, even after candidate use.
            for name in list(sys.modules):
                if name == 'kapampangan_morphbpe_runtime' or name.startswith('kapampangan_morphbpe_runtime.'):
                    del sys.modules[name]
            sys.path.insert(0, str(reference_bundle/'runtime'))
            ref_spec = importlib.util.spec_from_file_location('current32_verified_adapter', reference_bundle/'nllb_source_adapter.py')
            reference_helper = importlib.util.module_from_spec(ref_spec)
            ref_spec.loader.exec_module(reference_helper)
            reference_model, reference_source, reference_target = reference_helper.load_bundle(reference_bundle, DEVICE)
            reference_scores = WORK/'reference_evaluation'/'weighted_penalty32'
            for split in eval_splits:
                evaluate_selected(reference_model, reference_source, reference_target, splits[split], split,
                    reference_scores/split, reference_bundle, EXPECTED_DATA_SHA256,
                    DEVICE, BEAMS, MAX_NEW_TOKENS, SOURCE_LIMIT)
                compare_scores(OUT/'evaluation', reference_scores, split)
            del reference_model
            gc.collect(); torch.cuda.empty_cache()
        else:
            print('Current32 comparison skipped. Its reference package is optional.')
        """, code=True)]
    # Reload the candidate's own runtime after any reference evaluation rerun.
    reload_index = next(i for i, c in enumerate(cells) if c["source"].startswith("reload_info ="))
    cells[reload_index]["source"] = substitute(cells[reload_index]["source"], "    saved_spec = ",
        "    for name in list(sys.modules):\n        if name == 'kapampangan_morphbpe_runtime' or name.startswith('kapampangan_morphbpe_runtime.'):\n            del sys.modules[name]\n    sys.path.insert(0, str(OUT/'runtime'))\n    saved_spec = ")
    for index, cell in enumerate(cells):
        cell["source"] = cell["source"].replace(".read_text()", ".read_text(encoding='utf-8')")
        cell["id"] = f"infix{penalty}-{index:02d}"
        if cell["cell_type"] == "code":
            compile(cell["source"], f"{notebook_name}:cell-{index}", "exec")
    notebook["metadata"]["colab"]["name"] = notebook_name
    return notebook_name, notebook


def build_reference(baseline):
    source = ROOT / "nllb/checkpoints/morph_bpe"
    info = json.loads((source / "manifest.json").read_text())
    if (info["tokenizer_variant"] != "weighted_penalty32" or info["crossing_penalty"] != 32 or
            info["weighted_penalty_used"] is not True or info["cfg"] != baseline["cfg"] or
            info["identity"]["data_sha256"] != EXPECTED_DATA or info["training_status"] != "completed"):
        raise ValueError("Installed reference must be current weighted32 with matched recipe")
    files = {}
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if (not path.is_file() or any(p in ("__pycache__", "resume_backups", "evaluation") for p in rel.parts)
                or path.suffix in (".pt", ".pyc", ".zip")):
            continue
        files["morph_bpe/" + rel.as_posix()] = path.read_bytes()
    package = dict(package_kind="current_weighted32_translation_reference", format_version=1,
                   tokenizer_variant="weighted_penalty32", crossing_penalty=32,
                   initialization_source=False, resume_supported=False,
                   weights_sha256=sha(files["morph_bpe/best_source.safetensors"]),
                   files={name: sha(data) for name, data in sorted(files.items())})
    files["reference_package_manifest.json"] = blob(package)
    path = DESTINATION / "current_weighted32_reference.zip"
    return dict(path=path, zip_sha256=write_zip(path, files),
                manifest_sha256=sha(files["reference_package_manifest.json"]),
                weights_sha256=package["weights_sha256"], files=len(files))


def build(csv_path=None, artifact_root=DEFAULT_ARTIFACT_ROOT):
    DESTINATION.mkdir(parents=True, exist_ok=True)
    plain = ROOT / "nllb/checkpoints/plain_bpe"
    morph = ROOT / "nllb/checkpoints/morph_bpe"
    baseline = json.loads((plain / "manifest.json").read_text())
    if csv_path:
        csv_bytes = Path(csv_path).read_bytes()
    else:
        with zipfile.ZipFile(ROOT / "nllb/penalty32_training/penalty32_training_inputs.zip") as archive:
            csv_bytes = archive.read("data/kpm_tgl_cleaned.csv")
    if sha(csv_bytes) != EXPECTED_DATA or baseline["identity"]["data_sha256"] != EXPECTED_DATA:
        raise ValueError("Dataset bytes differ from the matched installed baseline")
    reference = build_reference(baseline)
    result = []
    for penalty, fingerprint in VARIANTS.items():
        artifact = Path(artifact_root) / f"penalty-{penalty}" / f"infix-only-penalty{penalty}"
        validate_variant_artifact(artifact / "tokenizer-manifest.json", artifact / "tokenizer.json", penalty, fingerprint)
        files = {"data/kpm_tgl_cleaned.csv": csv_bytes}
        for name in ("training_support.py", "evaluation_support.py"):
            files[name] = (HERE / name).read_bytes()
        files["nllb_source_adapter.py"] = (morph / "nllb_source_adapter.py").read_bytes()
        if sha(files["nllb_source_adapter.py"]) != baseline["identity"]["helper_sha256"]:
            raise ValueError("Training helper changed from matched baseline")
        for path in sorted(artifact.iterdir()):
            if path.is_file():
                files["source_artifact/" + path.name] = path.read_bytes()
        runtime = ROOT / "webapp/backend/tokenizer/kapampangan_morphbpe_runtime"
        for name in ("__init__.py", "tokenizer.py"):
            files["runtime/kapampangan_morphbpe_runtime/" + name] = (runtime / name).read_bytes()
        for path in sorted((plain / "target_tokenizer").iterdir()):
            if path.is_file():
                files["target_tokenizer/" + path.name] = path.read_bytes()
        for name in ("manifest.json", "data_audit.json", "split_manifest.json", "history.json", "tokenization_audit.json"):
            files["reference/plain_bpe/" + name] = (plain / name).read_bytes()
        for name in ("manifest.json", "history.json"):
            files["reference/morph_bpe/" + name] = (morph / name).read_bytes()
        package = dict(package_kind="infix_first_source_training", format_version=1,
                       **variant_fields(penalty), tokenizer_fingerprint=fingerprint,
                       expected_data_sha256=EXPECTED_DATA, csv_included=True,
                       trained_source_weights_included=False, template_notebook_sha256=TEMPLATE_SHA,
                       files={name: sha(data) for name, data in sorted(files.items())})
        files["package_manifest.json"] = blob(package)
        package_name = f"infix_first_penalty{penalty}_training_inputs.zip"
        archive_path = DESTINATION / package_name
        checksum = write_zip(archive_path, files)
        name, notebook = make_notebook(penalty, checksum, sha(files["package_manifest.json"]), reference)
        notebook_path = ROOT / "notebooks" / name
        notebook_path.write_bytes(blob(notebook))
        (DESTINATION / name).write_bytes(notebook_path.read_bytes())
        result.append(dict(penalty=penalty, notebook=name, notebook_sha256=sha(notebook_path.read_bytes()),
                           package=package_name, package_sha256=checksum, package_bytes=archive_path.stat().st_size,
                           package_files=len(files), tokenizer_fingerprint=fingerprint, artifact_source=str(artifact)))
    (DESTINATION / "README.md").write_bytes((HERE / "README.md").read_bytes())
    names = ["README.md", "current_weighted32_reference.zip"]
    names += [name for r in result for name in (r["notebook"], r["package"])]
    sums = "".join(sha((DESTINATION / name).read_bytes()) + "  " + name + "\n" for name in names)
    (DESTINATION / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    bundle_files = {name: (DESTINATION / name).read_bytes() for name in names + ["SHA256SUMS.txt"]}
    all_path = DESTINATION / "ALL_FILES.zip"
    all_sha = write_zip(all_path, bundle_files)
    manifest = dict(variants=result, current32_reference={k: str(v) if isinstance(v, Path) else v for k, v in reference.items()},
                    delivery_zip=str(all_path), delivery_sha256=all_sha,
                    gpu_training_executed=False, translation_scores_generated=False)
    (DESTINATION / "BUILD_MANIFEST.json").write_bytes(blob(manifest))
    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, help="Optional original matched CSV; otherwise reuse exact bytes from old input ZIP")
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    args = parser.parse_args()
    build(args.csv, args.artifact_root)
