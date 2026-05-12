import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.SecureRandom;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

import org.bouncycastle.util.BigIntegers;

public final class BouncyCastlePrimeSampleBehaviorProbe {
    private static final String PROBE_NAME = "bouncycastle-prime-sample-behavior-probe";
    private static final String ARTIFACT_ORIGIN = "source-build";
    private static final String BC_SOURCE_TAG = "r1rv83";
    private static final String BC_SOURCE_COMMIT = "d4cc9614fc849e840ffdc7941f4a2941131d0c9c";
    private static final String BCPROV_ARTIFACT = "bcprov-jdk18on";
    private static final String BCPROV_VERSION = "1.83";
    private static final String SECURE_RANDOM_ALGORITHM = "SHA1PRNG";
    private static final String DEFAULT_OUTPUT_PATH =
        "results/bcprov-jdk18on-1.83-source-r1rv83-prime-sample-behavior-seed-byte-42.json";
    private static final String DEFAULT_REPORT_NAME = "BOUNCY_CASTLE_PRIME_SAMPLE_BEHAVIOR_REPORT.md";
    private static final int FIDELITY_SAMPLE_COUNT = 1024;
    private static final int HISTOGRAM_BUCKET_COUNT = 64;
    private static final int CDF_SCALE = 12;
    private static final int STAT_SCALE = 12;
    private static final int PRIMARY_LIMIT = 200003;
    private static final int PRIMARY_START_EXCLUSIVE = 743;
    private static final int TAIL_LIMIT = 300007;
    private static final int TAIL_START_EXCLUSIVE = 200003;
    private static final int CHUNK_SIZE = 256;
    private static final byte[] SEED_BYTES = new byte[] {42};
    private static final BigInteger ONE = BigInteger.ONE;
    private static final BigInteger TWO = BigInteger.valueOf(2L);
    private static final BigInteger THREE = BigInteger.valueOf(3L);
    private static final BigInteger SMALL_PRIMES_PRODUCT = new BigInteger(
        "8138e8a0fcf3a4e84a771d40fd305d7f4aa59306d7251de54d98af8fe95729a1f"
            + "73d893fa424cd2edc8636a6c3285e022b0e3866a565ae8108eed8591cd4fe8d2"
            + "ce86165a978d719ebf647f362d33fca29cd179fb42401cbaf3df0c614056f9c8"
            + "f3cfd51e474afb6bc6974f78db8aba8e9e517fded658591ab7502bd41849462f",
        16
    );
    private static final int MAX_SMALL = BigInteger.valueOf(743L).bitLength();
    private static final int[] CDF_DECILES_NUMERATORS = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    private static final int[] MOD210_ADMISSIBLE_RESIDUES = buildAdmissibleResidues();
    private static final PanelConfig[] PANELS = new PanelConfig[] {
        new PanelConfig("panel_256", 256, 16384),
        new PanelConfig("panel_2048", 2048, 4096),
    };

    private BouncyCastlePrimeSampleBehaviorProbe() {
    }

    public static void main(String[] args) throws Exception {
        if (args.length > 1) {
            throw new IllegalArgumentException("expected zero or one output path argument");
        }

        Path outputPath = args.length == 1 ? Path.of(args[0]) : Path.of(DEFAULT_OUTPUT_PATH);
        Files.createDirectories(outputPath.toAbsolutePath().getParent());
        Path reportPath = outputPath.toAbsolutePath().getParent().resolve(DEFAULT_REPORT_NAME);

        String bcBuildJavaVersion = requiredProperty("bc.build.java.version");
        String bcRuntimeJavaVersion = requiredProperty("bc.runtime.java.version");
        String bcBuiltJarSha256 = requiredProperty("bc.built.jar.sha256");

        Instant startedAt = Instant.now();

        ChunkedPrimeTable primaryTable = new ChunkedPrimeTable(PRIMARY_LIMIT, CHUNK_SIZE, PRIMARY_START_EXCLUSIVE);
        ChunkedPrimeTable tailTable = new ChunkedPrimeTable(TAIL_LIMIT, CHUNK_SIZE, TAIL_START_EXCLUSIVE);

        List<PanelResult> panelResults = new ArrayList<PanelResult>(PANELS.length);
        for (PanelConfig panel : PANELS) {
            panelResults.add(evaluatePanel(panel, primaryTable, tailTable));
        }

        Instant completedAt = Instant.now();

        Files.writeString(
            outputPath,
            buildJson(
                outputPath,
                reportPath,
                startedAt,
                completedAt,
                bcBuildJavaVersion,
                bcRuntimeJavaVersion,
                bcBuiltJarSha256,
                panelResults
            )
        );
        Files.writeString(
            reportPath,
            buildMarkdownReport(
                outputPath,
                reportPath,
                completedAt,
                panelResults
            )
        );

        System.out.println("wrote " + outputPath.toAbsolutePath());
        System.out.println("wrote " + reportPath.toAbsolutePath());
    }

    private static PanelResult evaluatePanel(
        PanelConfig panel,
        ChunkedPrimeTable primaryTable,
        ChunkedPrimeTable tailTable
    ) throws Exception {
        FidelityResult fidelity = validateFidelity(panel.bitLength);
        GeneratorSummary baseline = sampleGenerator(panel.bitLength, panel.sampleCount, GeneratorMode.BASELINE_HELPER, primaryTable, tailTable);
        GeneratorSummary dci = sampleGenerator(panel.bitLength, panel.sampleCount, GeneratorMode.DCI_PREFILTER_HELPER, primaryTable, tailTable);
        DriftSummary drift = buildDriftSummary(baseline, dci);
        return new PanelResult(panel, fidelity, baseline, dci, drift);
    }

    private static FidelityResult validateFidelity(int bitLength) throws Exception {
        SecureRandom actualRandom = seededRandom();
        SecureRandom helperRandom = seededRandom();

        for (int index = 0; index < FIDELITY_SAMPLE_COUNT; index++) {
            BigInteger actual = BigIntegers.createRandomPrime(bitLength, 1, actualRandom);
            GenerationOutcome helper = generateOne(bitLength, helperRandom, GeneratorMode.BASELINE_HELPER, null, null);
            if (!actual.equals(helper.output)) {
                throw new IllegalStateException(
                    "baseline helper mismatch at bit length " + bitLength + " output index " + index
                );
            }
        }

        return new FidelityResult(true, null);
    }

    private static GeneratorSummary sampleGenerator(
        int bitLength,
        int sampleCount,
        GeneratorMode mode,
        ChunkedPrimeTable primaryTable,
        ChunkedPrimeTable tailTable
    ) throws Exception {
        SecureRandom random = seededRandom();
        List<BigInteger> outputs = new ArrayList<BigInteger>(sampleCount);
        int[] rawStarts = new int[sampleCount];
        int[] walkIncrements = new int[sampleCount];

        long totalRawStarts = 0L;
        long totalWalkIncrements = 0L;
        int totalConcreteFactorRejects = 0;
        int primaryIntervalRejects = 0;
        int tailIntervalRejects = 0;

        for (int i = 0; i < sampleCount; i++) {
            GenerationOutcome outcome = generateOne(bitLength, random, mode, primaryTable, tailTable);
            outputs.add(outcome.output);
            rawStarts[i] = outcome.rawStartsConsumed;
            walkIncrements[i] = outcome.walkIncrements;
            totalRawStarts += outcome.rawStartsConsumed;
            totalWalkIncrements += outcome.walkIncrements;
            totalConcreteFactorRejects += outcome.totalConcreteFactorRejects;
            primaryIntervalRejects += outcome.primaryIntervalRejects;
            tailIntervalRejects += outcome.tailIntervalRejects;
        }

        return GeneratorSummary.from(
            outputs,
            rawStarts,
            walkIncrements,
            totalRawStarts,
            totalWalkIncrements,
            totalConcreteFactorRejects,
            primaryIntervalRejects,
            tailIntervalRejects,
            bitLength,
            sampleCount
        );
    }

    private static GenerationOutcome generateOne(
        int bitLength,
        SecureRandom random,
        GeneratorMode mode,
        ChunkedPrimeTable primaryTable,
        ChunkedPrimeTable tailTable
    ) {
        int rawStartsConsumed = 0;
        int walkIncrements = 0;
        int totalConcreteFactorRejects = 0;
        int primaryIntervalRejects = 0;
        int tailIntervalRejects = 0;

        for (;;) {
            rawStartsConsumed++;

            BigInteger candidate = createRawCandidate(bitLength, random);
            if (bitLength > MAX_SMALL) {
                while (!candidate.gcd(SMALL_PRIMES_PRODUCT).equals(ONE)) {
                    candidate = candidate.add(TWO);
                    walkIncrements++;
                }
            }

            if (mode == GeneratorMode.DCI_PREFILTER_HELPER) {
                BigInteger primaryFactor = primaryTable.findFactor(candidate);
                if (primaryFactor != null) {
                    totalConcreteFactorRejects++;
                    primaryIntervalRejects++;
                    continue;
                }

                BigInteger tailFactor = tailTable.findFactor(candidate);
                if (tailFactor != null) {
                    totalConcreteFactorRejects++;
                    tailIntervalRejects++;
                    continue;
                }
            }

            if (candidate.isProbablePrime(1)) {
                return new GenerationOutcome(
                    candidate,
                    rawStartsConsumed,
                    walkIncrements,
                    totalConcreteFactorRejects,
                    primaryIntervalRejects,
                    tailIntervalRejects
                );
            }
        }
    }

    private static BigInteger createRawCandidate(int bitLength, SecureRandom random) {
        if (bitLength < 2) {
            throw new IllegalArgumentException("bitLength < 2");
        }

        if (bitLength == 2) {
            return random.nextInt() < 0 ? TWO : THREE;
        }

        byte[] base = createRandom(bitLength, random);
        int xBits = 8 * base.length - bitLength;
        byte lead = (byte)(1 << (7 - xBits));

        base[0] |= lead;
        base[base.length - 1] |= 0x01;
        return new BigInteger(1, base);
    }

    private static byte[] createRandom(int bitLength, SecureRandom random) {
        int nBytes = (bitLength + 7) / 8;
        byte[] rv = new byte[nBytes];
        random.nextBytes(rv);
        int xBits = 8 * nBytes - bitLength;
        rv[0] &= (byte)(255 >>> xBits);
        return rv;
    }

    private static DriftSummary buildDriftSummary(GeneratorSummary baseline, GeneratorSummary dci) {
        double histogramTvd = totalVariationDistance(baseline.normalizedHistogramCounts, dci.normalizedHistogramCounts, baseline.sampleCount);
        double mod30Tvd = totalVariationDistance(baseline.mod30Counts, dci.mod30Counts, baseline.sampleCount);
        double mod210Tvd = totalVariationDistance(baseline.mod210AdmissibleCounts, dci.mod210AdmissibleCounts, baseline.sampleCount);

        double maxTvd = histogramTvd;
        String dominantMetric = "normalized_histogram";
        int[] dominantBaselineCounts = baseline.normalizedHistogramCounts;
        int[] dominantDciCounts = dci.normalizedHistogramCounts;

        if (mod30Tvd > maxTvd) {
            maxTvd = mod30Tvd;
            dominantMetric = "mod_30";
            dominantBaselineCounts = baseline.mod30Counts;
            dominantDciCounts = dci.mod30Counts;
        }

        if (mod210Tvd > maxTvd) {
            maxTvd = mod210Tvd;
            dominantMetric = "mod_210_admissible";
            dominantBaselineCounts = baseline.mod210AdmissibleCounts;
            dominantDciCounts = dci.mod210AdmissibleCounts;
        }

        String visibilityLabel;
        if (maxTvd >= 0.02) {
            visibilityLabel = "visible";
        }
        else if (maxTvd >= 0.005) {
            visibilityLabel = "slight";
        }
        else {
            visibilityLabel = "not_obvious";
        }

        double topFiveShare = dominantMetricTopFiveShare(dominantBaselineCounts, dominantDciCounts, baseline.sampleCount);
        String concentrationLabel = topFiveShare >= 0.60 ? "concentrated" : "diffuse";

        return new DriftSummary(
            histogramTvd,
            mod30Tvd,
            mod210Tvd,
            visibilityLabel,
            concentrationLabel,
            dominantMetric,
            topFiveShare
        );
    }

    private static double dominantMetricTopFiveShare(int[] baselineCounts, int[] dciCounts, int sampleCount) {
        List<Double> absoluteDeltas = new ArrayList<Double>(baselineCounts.length);
        double totalAbsoluteDelta = 0.0;
        for (int i = 0; i < baselineCounts.length; i++) {
            double delta = Math.abs(((double) baselineCounts[i] / sampleCount) - ((double) dciCounts[i] / sampleCount));
            absoluteDeltas.add(Double.valueOf(delta));
            totalAbsoluteDelta += delta;
        }
        if (totalAbsoluteDelta == 0.0) {
            return 0.0;
        }
        absoluteDeltas.sort(Comparator.reverseOrder());
        double topFive = 0.0;
        for (int i = 0; i < Math.min(5, absoluteDeltas.size()); i++) {
            topFive += absoluteDeltas.get(i).doubleValue();
        }
        return topFive / totalAbsoluteDelta;
    }

    private static double totalVariationDistance(int[] baselineCounts, int[] dciCounts, int sampleCount) {
        double l1 = 0.0;
        for (int i = 0; i < baselineCounts.length; i++) {
            l1 += Math.abs(((double) baselineCounts[i] / sampleCount) - ((double) dciCounts[i] / sampleCount));
        }
        return 0.5 * l1;
    }

    private static int[] buildAdmissibleResidues() {
        List<Integer> residues = new ArrayList<Integer>();
        for (int residue = 0; residue < 210; residue++) {
            if (BigInteger.valueOf(residue).gcd(BigInteger.valueOf(210L)).equals(ONE)) {
                residues.add(Integer.valueOf(residue));
            }
        }

        int[] result = new int[residues.size()];
        for (int i = 0; i < residues.size(); i++) {
            result[i] = residues.get(i).intValue();
        }
        return result;
    }

    private static SecureRandom seededRandom() throws Exception {
        SecureRandom random = SecureRandom.getInstance(SECURE_RANDOM_ALGORITHM);
        random.setSeed(SEED_BYTES);
        return random;
    }

    private static String buildJson(
        Path outputPath,
        Path reportPath,
        Instant startedAt,
        Instant completedAt,
        String bcBuildJavaVersion,
        String bcRuntimeJavaVersion,
        String bcBuiltJarSha256,
        List<PanelResult> panelResults
    ) {
        StringBuilder builder = new StringBuilder();
        builder.append("{\n");
        builder.append("  \"probe\": \"").append(PROBE_NAME).append("\",\n");
        builder.append("  \"output_path\": \"").append(escapeJson(outputPath.toString())).append("\",\n");
        builder.append("  \"report_path\": \"").append(escapeJson(reportPath.toString())).append("\",\n");
        builder.append("  \"started_at_utc\": \"").append(startedAt).append("\",\n");
        builder.append("  \"completed_at_utc\": \"").append(completedAt).append("\",\n");
        builder.append("  \"provenance\": {\n");
        builder.append("    \"artifact_origin\": \"").append(ARTIFACT_ORIGIN).append("\",\n");
        builder.append("    \"bc_source_tag\": \"").append(BC_SOURCE_TAG).append("\",\n");
        builder.append("    \"bc_source_commit\": \"").append(BC_SOURCE_COMMIT).append("\",\n");
        builder.append("    \"bc_build_java_version\": \"").append(escapeJson(bcBuildJavaVersion)).append("\",\n");
        builder.append("    \"bc_runtime_java_version\": \"").append(escapeJson(bcRuntimeJavaVersion)).append("\",\n");
        builder.append("    \"bc_built_jar_sha256\": \"").append(escapeJson(bcBuiltJarSha256)).append("\"\n");
        builder.append("  },\n");
        builder.append("  \"configuration\": {\n");
        builder.append("    \"bcprov_artifact\": \"").append(BCPROV_ARTIFACT).append("\",\n");
        builder.append("    \"bcprov_version\": \"").append(BCPROV_VERSION).append("\",\n");
        builder.append("    \"candidate_source\": \"org.bouncycastle.util.BigIntegers.createRandomPrime\",\n");
        builder.append("    \"certainty\": 1,\n");
        builder.append("    \"secure_random_algorithm\": \"").append(SECURE_RANDOM_ALGORITHM).append("\",\n");
        builder.append("    \"seed_bytes_decimal\": [42],\n");
        builder.append("    \"fidelity_sample_count\": ").append(FIDELITY_SAMPLE_COUNT).append(",\n");
        builder.append("    \"histogram_bucket_count\": ").append(HISTOGRAM_BUCKET_COUNT).append(",\n");
        builder.append("    \"primary_interval_start_exclusive\": ").append(PRIMARY_START_EXCLUSIVE).append(",\n");
        builder.append("    \"primary_interval_limit\": ").append(PRIMARY_LIMIT).append(",\n");
        builder.append("    \"tail_interval_start_exclusive\": ").append(TAIL_START_EXCLUSIVE).append(",\n");
        builder.append("    \"tail_interval_limit\": ").append(TAIL_LIMIT).append(",\n");
        builder.append("    \"chunk_size\": ").append(CHUNK_SIZE).append(",\n");
        builder.append("    \"mod210_admissible_residues\": ");
        appendIntArray(builder, MOD210_ADMISSIBLE_RESIDUES, 4);
        builder.append(",\n");
        builder.append("    \"java_version\": \"").append(escapeJson(System.getProperty("java.version"))).append("\",\n");
        builder.append("    \"java_vendor\": \"").append(escapeJson(System.getProperty("java.vendor"))).append("\",\n");
        builder.append("    \"os_name\": \"").append(escapeJson(System.getProperty("os.name"))).append("\",\n");
        builder.append("    \"os_arch\": \"").append(escapeJson(System.getProperty("os.arch"))).append("\"\n");
        builder.append("  },\n");
        builder.append("  \"panels\": [\n");
        for (int i = 0; i < panelResults.size(); i++) {
            appendPanelJson(builder, panelResults.get(i), i + 1 < panelResults.size());
        }
        builder.append("  ]\n");
        builder.append("}\n");
        return builder.toString();
    }

    private static void appendPanelJson(StringBuilder builder, PanelResult panel, boolean trailingComma) {
        builder.append("    {\n");
        builder.append("      \"name\": \"").append(panel.config.name).append("\",\n");
        builder.append("      \"bit_length\": ").append(panel.config.bitLength).append(",\n");
        builder.append("      \"sample_count\": ").append(panel.config.sampleCount).append(",\n");
        builder.append("      \"fidelity\": {\n");
        builder.append("        \"checked_outputs\": ").append(FIDELITY_SAMPLE_COUNT).append(",\n");
        builder.append("        \"baseline_helper_matches_actual_bc\": ").append(panel.fidelity.matchesActualBc).append(",\n");
        builder.append("        \"mismatch_index\": ");
        if (panel.fidelity.mismatchIndex == null) {
            builder.append("null\n");
        }
        else {
            builder.append(panel.fidelity.mismatchIndex.intValue()).append("\n");
        }
        builder.append("      },\n");
        builder.append("      \"baseline_helper\": ");
        appendGeneratorJson(builder, panel.baseline);
        builder.append(",\n");
        builder.append("      \"dci_prefilter_helper\": ");
        appendGeneratorJson(builder, panel.dciPrefilter);
        builder.append(",\n");
        builder.append("      \"drift\": {\n");
        builder.append("        \"normalized_histogram_tvd\": ")
            .append(formatDouble(panel.drift.normalizedHistogramTvd)).append(",\n");
        builder.append("        \"mod_30_tvd\": ")
            .append(formatDouble(panel.drift.mod30Tvd)).append(",\n");
        builder.append("        \"mod_210_admissible_tvd\": ")
            .append(formatDouble(panel.drift.mod210AdmissibleTvd)).append(",\n");
        builder.append("        \"coarse_visibility_label\": \"")
            .append(panel.drift.coarseVisibilityLabel).append("\",\n");
        builder.append("        \"coarse_concentration_label\": \"")
            .append(panel.drift.coarseConcentrationLabel).append("\",\n");
        builder.append("        \"dominant_metric\": \"").append(panel.drift.dominantMetric).append("\",\n");
        builder.append("        \"dominant_metric_top_five_contribution_share\": ")
            .append(formatDouble(panel.drift.dominantMetricTopFiveContributionShare)).append("\n");
        builder.append("      }\n");
        builder.append("    }");
        if (trailingComma) {
            builder.append(",");
        }
        builder.append("\n");
    }

    private static void appendGeneratorJson(StringBuilder builder, GeneratorSummary summary) {
        builder.append("{\n");
        builder.append("        \"sample_count\": ").append(summary.sampleCount).append(",\n");
        builder.append("        \"outputs_above_full_interval\": ").append(summary.outputsAboveFullInterval).append(",\n");
        builder.append("        \"normalized_position_mean\": ").append(formatBigDecimal(summary.normalizedPositionMean)).append(",\n");
        builder.append("        \"normalized_position_median\": ").append(formatBigDecimal(summary.normalizedPositionMedian)).append(",\n");
        builder.append("        \"raw_starts_mean\": ").append(formatBigDecimal(summary.rawStartsMean)).append(",\n");
        builder.append("        \"raw_starts_median\": ").append(formatBigDecimal(summary.rawStartsMedian)).append(",\n");
        builder.append("        \"walk_increments_mean\": ").append(formatBigDecimal(summary.walkIncrementsMean)).append(",\n");
        builder.append("        \"walk_increments_median\": ").append(formatBigDecimal(summary.walkIncrementsMedian)).append(",\n");
        builder.append("        \"total_raw_starts_consumed\": ").append(summary.totalRawStartsConsumed).append(",\n");
        builder.append("        \"total_walk_increments\": ").append(summary.totalWalkIncrements).append(",\n");
        builder.append("        \"total_concrete_factor_rejects\": ").append(summary.totalConcreteFactorRejects).append(",\n");
        builder.append("        \"primary_interval_rejects\": ").append(summary.primaryIntervalRejects).append(",\n");
        builder.append("        \"tail_interval_rejects\": ").append(summary.tailIntervalRejects).append(",\n");
        builder.append("        \"normalized_histogram_counts\": ");
        appendIntArray(builder, summary.normalizedHistogramCounts, 8);
        builder.append(",\n");
        builder.append("        \"cdf_at_deciles\": [\n");
        for (int i = 0; i < summary.cdfAtDeciles.length; i++) {
            builder.append("          {\"checkpoint\": ")
                .append(formatDouble(((double) CDF_DECILES_NUMERATORS[i]) / 10.0))
                .append(", \"cdf\": ")
                .append(formatDouble(summary.cdfAtDeciles[i]))
                .append("}");
            if (i + 1 < summary.cdfAtDeciles.length) {
                builder.append(",");
            }
            builder.append("\n");
        }
        builder.append("        ],\n");
        builder.append("        \"mod_30_counts\": ");
        appendIntArray(builder, summary.mod30Counts, 8);
        builder.append(",\n");
        builder.append("        \"mod_210_admissible_counts\": ");
        appendIntArray(builder, summary.mod210AdmissibleCounts, 8);
        builder.append("\n");
        builder.append("      }");
    }

    private static void appendIntArray(StringBuilder builder, int[] values, int indent) {
        String indentText = repeat(" ", indent);
        builder.append("[");
        if (values.length == 0) {
            builder.append("]");
            return;
        }
        builder.append("\n");
        for (int i = 0; i < values.length; i++) {
            builder.append(indentText).append(values[i]);
            if (i + 1 < values.length) {
                builder.append(",");
            }
            builder.append("\n");
        }
        builder.append(repeat(" ", Math.max(0, indent - 2))).append("]");
    }

    private static String buildMarkdownReport(
        Path outputPath,
        Path reportPath,
        Instant completedAt,
        List<PanelResult> panels
    ) {
        StringBuilder builder = new StringBuilder();
        builder.append("# Bouncy Castle Prime Sample Behavior Probe\n\n");
        builder.append("Date: ")
            .append(DateTimeFormatter.ISO_LOCAL_DATE.format(LocalDate.ofInstant(completedAt, ZoneOffset.UTC)))
            .append("\n\n");

        boolean allFidelityPass = true;
        for (PanelResult panel : panels) {
            allFidelityPass &= panel.fidelity.matchesActualBc;
        }

        builder.append("The baseline helper ");
        builder.append(allFidelityPass ? "exactly reproduces" : "does not reproduce");
        builder.append(" `BigIntegers.createRandomPrime(bitLength, 1, random)` for the first `1024` outputs on every panel.\n\n");

        builder.append("The DCI-prefiltered helper is characterized against that matched baseline helper on coarse output metrics. ");
        builder.append("These labels are descriptive only and come from the report's coarse TVD and concentration heuristics.\n\n");

        builder.append("| Panel | Fidelity | Histogram TVD | Mod 30 TVD | Mod 210 TVD | Visibility | Pattern |\n");
        builder.append("|---|---|---:|---:|---:|---|---|\n");
        for (PanelResult panel : panels) {
            builder.append("| `").append(panel.config.bitLength).append("` bits | `")
                .append(panel.fidelity.matchesActualBc ? "exact" : "mismatch")
                .append("` | `").append(formatDouble(panel.drift.normalizedHistogramTvd))
                .append("` | `").append(formatDouble(panel.drift.mod30Tvd))
                .append("` | `").append(formatDouble(panel.drift.mod210AdmissibleTvd))
                .append("` | `").append(panel.drift.coarseVisibilityLabel)
                .append("` | `").append(panel.drift.coarseConcentrationLabel)
                .append("` |\n");
        }
        builder.append("\n");

        builder.append("| Panel | Prefilter Rejects | Raw Starts Mean (Before -> After) | Walk Increments Mean (Before -> After) |\n");
        builder.append("|---|---:|---:|---:|\n");
        for (PanelResult panel : panels) {
            builder.append("| `").append(panel.config.bitLength).append("` bits | `")
                .append(panel.dciPrefilter.totalConcreteFactorRejects)
                .append("` (`")
                .append(panel.dciPrefilter.primaryIntervalRejects)
                .append("` primary, `")
                .append(panel.dciPrefilter.tailIntervalRejects)
                .append("` tail) | `")
                .append(formatBigDecimal(panel.baseline.rawStartsMean))
                .append(" -> ")
                .append(formatBigDecimal(panel.dciPrefilter.rawStartsMean))
                .append("` | `")
                .append(formatBigDecimal(panel.baseline.walkIncrementsMean))
                .append(" -> ")
                .append(formatBigDecimal(panel.dciPrefilter.walkIncrementsMean))
                .append("` |\n");
        }
        builder.append("\n");

        for (PanelResult panel : panels) {
            builder.append("## ").append(panel.config.bitLength).append("-Bit Panel\n\n");
            builder.append("Coarse drift is `").append(panel.drift.coarseVisibilityLabel)
                .append("`, and the dominant metric is `")
                .append(panel.drift.dominantMetric)
                .append("` with top-five contribution share `")
                .append(formatDouble(panel.drift.dominantMetricTopFiveContributionShare))
                .append("`, so the reported pattern is `")
                .append(panel.drift.coarseConcentrationLabel)
                .append("`.\n\n");

            builder.append("Largest changes in the dominant metric:\n");
            for (MetricChange change : topMetricChanges(panel)) {
                builder.append("- `").append(change.label).append("`: baseline `")
                    .append(change.baselineCount)
                    .append("`, after `")
                    .append(change.afterCount)
                    .append("`, |delta| `")
                    .append(formatDouble(change.absoluteProbabilityDelta))
                    .append("`\n");
            }
            builder.append("\n");
        }

        builder.append("Artifacts:\n");
        builder.append("- [`")
            .append(outputPath.getFileName())
            .append("`](./")
            .append(outputPath.getFileName())
            .append(")\n");
        builder.append("- [`")
            .append(reportPath.getFileName())
            .append("`](./")
            .append(reportPath.getFileName())
            .append(")\n");
        return builder.toString();
    }

    private static List<MetricChange> topMetricChanges(PanelResult panel) {
        if ("mod_30".equals(panel.drift.dominantMetric)) {
            return topResidueChanges(panel.baseline.mod30Counts, panel.dciPrefilter.mod30Counts, panel.baseline.sampleCount, 30, false);
        }
        if ("mod_210_admissible".equals(panel.drift.dominantMetric)) {
            return topResidueChanges(panel.baseline.mod210AdmissibleCounts, panel.dciPrefilter.mod210AdmissibleCounts, panel.baseline.sampleCount, 210, true);
        }
        return topHistogramChanges(panel.baseline.normalizedHistogramCounts, panel.dciPrefilter.normalizedHistogramCounts, panel.baseline.sampleCount);
    }

    private static List<MetricChange> topHistogramChanges(int[] baselineCounts, int[] afterCounts, int sampleCount) {
        List<MetricChange> changes = new ArrayList<MetricChange>(baselineCounts.length);
        for (int i = 0; i < baselineCounts.length; i++) {
            String label = "bucket " + i + " [" + formatDouble(i / 64.0) + ", " + formatDouble((i + 1) / 64.0) + ")";
            double delta = Math.abs(((double) baselineCounts[i] / sampleCount) - ((double) afterCounts[i] / sampleCount));
            changes.add(new MetricChange(label, baselineCounts[i], afterCounts[i], delta));
        }
        changes.sort(Comparator.comparingDouble((MetricChange value) -> value.absoluteProbabilityDelta).reversed());
        return changes.subList(0, Math.min(5, changes.size()));
    }

    private static List<MetricChange> topResidueChanges(
        int[] baselineCounts,
        int[] afterCounts,
        int sampleCount,
        int modulus,
        boolean admissibleOnly
    ) {
        List<MetricChange> changes = new ArrayList<MetricChange>(baselineCounts.length);
        int[] residues = admissibleOnly ? MOD210_ADMISSIBLE_RESIDUES : null;
        for (int i = 0; i < baselineCounts.length; i++) {
            int residue = admissibleOnly ? residues[i] : i;
            String label = "residue " + residue + " (mod " + modulus + ")";
            double delta = Math.abs(((double) baselineCounts[i] / sampleCount) - ((double) afterCounts[i] / sampleCount));
            changes.add(new MetricChange(label, baselineCounts[i], afterCounts[i], delta));
        }
        changes.sort(Comparator.comparingDouble((MetricChange value) -> value.absoluteProbabilityDelta).reversed());
        return changes.subList(0, Math.min(5, changes.size()));
    }

    private static String requiredProperty(String name) {
        String value = System.getProperty(name);
        if (value == null || value.isEmpty()) {
            throw new IllegalStateException("missing required system property: " + name);
        }
        return value;
    }

    private static BigDecimal normalizedPosition(BigInteger value, int bitLength) {
        BigInteger lower = ONE.shiftLeft(bitLength - 1);
        BigInteger range = ONE.shiftLeft(bitLength - 1);
        BigInteger position = value.subtract(lower);
        return divide(position, range, STAT_SCALE);
    }

    private static BigDecimal divide(BigInteger numerator, BigInteger denominator, int scale) {
        return new BigDecimal(numerator).divide(new BigDecimal(denominator), scale, RoundingMode.HALF_UP);
    }

    private static BigDecimal mean(int[] values) {
        long total = 0L;
        for (int value : values) {
            total += value;
        }
        return new BigDecimal(total).divide(new BigDecimal(values.length), STAT_SCALE, RoundingMode.HALF_UP);
    }

    private static BigDecimal median(int[] values) {
        int[] copy = values.clone();
        Arrays.sort(copy);
        if ((copy.length % 2) == 1) {
            return new BigDecimal(copy[copy.length / 2]);
        }
        BigDecimal left = new BigDecimal(copy[(copy.length / 2) - 1]);
        BigDecimal right = new BigDecimal(copy[copy.length / 2]);
        return left.add(right).divide(BigDecimal.valueOf(2L), STAT_SCALE, RoundingMode.HALF_UP);
    }

    private static String formatDouble(double value) {
        return String.format(Locale.US, "%.12f", value);
    }

    private static String formatBigDecimal(BigDecimal value) {
        return value.setScale(STAT_SCALE, RoundingMode.HALF_UP).toPlainString();
    }

    private static String escapeJson(String value) {
        return value.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    private static String repeat(String value, int count) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < count; i++) {
            builder.append(value);
        }
        return builder.toString();
    }

    private enum GeneratorMode {
        BASELINE_HELPER,
        DCI_PREFILTER_HELPER
    }

    private static final class PanelConfig {
        private final String name;
        private final int bitLength;
        private final int sampleCount;

        private PanelConfig(String name, int bitLength, int sampleCount) {
            this.name = name;
            this.bitLength = bitLength;
            this.sampleCount = sampleCount;
        }
    }

    private static final class FidelityResult {
        private final boolean matchesActualBc;
        private final Integer mismatchIndex;

        private FidelityResult(boolean matchesActualBc, Integer mismatchIndex) {
            this.matchesActualBc = matchesActualBc;
            this.mismatchIndex = mismatchIndex;
        }
    }

    private static final class GenerationOutcome {
        private final BigInteger output;
        private final int rawStartsConsumed;
        private final int walkIncrements;
        private final int totalConcreteFactorRejects;
        private final int primaryIntervalRejects;
        private final int tailIntervalRejects;

        private GenerationOutcome(
            BigInteger output,
            int rawStartsConsumed,
            int walkIncrements,
            int totalConcreteFactorRejects,
            int primaryIntervalRejects,
            int tailIntervalRejects
        ) {
            this.output = output;
            this.rawStartsConsumed = rawStartsConsumed;
            this.walkIncrements = walkIncrements;
            this.totalConcreteFactorRejects = totalConcreteFactorRejects;
            this.primaryIntervalRejects = primaryIntervalRejects;
            this.tailIntervalRejects = tailIntervalRejects;
        }
    }

    private static final class GeneratorSummary {
        private final int sampleCount;
        private final int outputsAboveFullInterval;
        private final BigDecimal normalizedPositionMean;
        private final BigDecimal normalizedPositionMedian;
        private final BigDecimal rawStartsMean;
        private final BigDecimal rawStartsMedian;
        private final BigDecimal walkIncrementsMean;
        private final BigDecimal walkIncrementsMedian;
        private final long totalRawStartsConsumed;
        private final long totalWalkIncrements;
        private final int totalConcreteFactorRejects;
        private final int primaryIntervalRejects;
        private final int tailIntervalRejects;
        private final int[] normalizedHistogramCounts;
        private final double[] cdfAtDeciles;
        private final int[] mod30Counts;
        private final int[] mod210AdmissibleCounts;

        private GeneratorSummary(
            int sampleCount,
            int outputsAboveFullInterval,
            BigDecimal normalizedPositionMean,
            BigDecimal normalizedPositionMedian,
            BigDecimal rawStartsMean,
            BigDecimal rawStartsMedian,
            BigDecimal walkIncrementsMean,
            BigDecimal walkIncrementsMedian,
            long totalRawStartsConsumed,
            long totalWalkIncrements,
            int totalConcreteFactorRejects,
            int primaryIntervalRejects,
            int tailIntervalRejects,
            int[] normalizedHistogramCounts,
            double[] cdfAtDeciles,
            int[] mod30Counts,
            int[] mod210AdmissibleCounts
        ) {
            this.sampleCount = sampleCount;
            this.outputsAboveFullInterval = outputsAboveFullInterval;
            this.normalizedPositionMean = normalizedPositionMean;
            this.normalizedPositionMedian = normalizedPositionMedian;
            this.rawStartsMean = rawStartsMean;
            this.rawStartsMedian = rawStartsMedian;
            this.walkIncrementsMean = walkIncrementsMean;
            this.walkIncrementsMedian = walkIncrementsMedian;
            this.totalRawStartsConsumed = totalRawStartsConsumed;
            this.totalWalkIncrements = totalWalkIncrements;
            this.totalConcreteFactorRejects = totalConcreteFactorRejects;
            this.primaryIntervalRejects = primaryIntervalRejects;
            this.tailIntervalRejects = tailIntervalRejects;
            this.normalizedHistogramCounts = normalizedHistogramCounts;
            this.cdfAtDeciles = cdfAtDeciles;
            this.mod30Counts = mod30Counts;
            this.mod210AdmissibleCounts = mod210AdmissibleCounts;
        }

        private static GeneratorSummary from(
            List<BigInteger> outputs,
            int[] rawStarts,
            int[] walkIncrements,
            long totalRawStartsConsumed,
            long totalWalkIncrements,
            int totalConcreteFactorRejects,
            int primaryIntervalRejects,
            int tailIntervalRejects,
            int bitLength,
            int sampleCount
        ) {
            BigInteger lower = ONE.shiftLeft(bitLength - 1);
            BigInteger upper = ONE.shiftLeft(bitLength);
            BigInteger range = ONE.shiftLeft(bitLength - 1);
            int[] histogramCounts = new int[HISTOGRAM_BUCKET_COUNT];
            int[] mod30Counts = new int[30];
            int[] mod210Counts = new int[MOD210_ADMISSIBLE_RESIDUES.length];
            int[] residueToAdmissibleIndex = buildResidueToAdmissibleIndex();
            int outputsAboveFullInterval = 0;
            BigInteger sumPositions = BigInteger.ZERO;

            List<BigInteger> sortedOutputs = new ArrayList<BigInteger>(outputs);
            Collections.sort(sortedOutputs);

            for (BigInteger output : outputs) {
                BigInteger position = output.subtract(lower);
                sumPositions = sumPositions.add(position);

                int bucket = position.shiftRight(bitLength - 7).intValue();
                if (output.compareTo(upper) >= 0) {
                    outputsAboveFullInterval++;
                }
                if (bucket < 0) {
                    bucket = 0;
                }
                if (bucket >= HISTOGRAM_BUCKET_COUNT) {
                    bucket = HISTOGRAM_BUCKET_COUNT - 1;
                }
                histogramCounts[bucket]++;

                mod30Counts[output.mod(BigInteger.valueOf(30L)).intValue()]++;
                int admissibleIndex = residueToAdmissibleIndex[output.mod(BigInteger.valueOf(210L)).intValue()];
                if (admissibleIndex >= 0) {
                    mod210Counts[admissibleIndex]++;
                }
            }

            BigDecimal normalizedPositionMean = divide(
                sumPositions,
                range.multiply(BigInteger.valueOf(sampleCount)),
                STAT_SCALE
            );

            BigDecimal normalizedPositionMedian;
            if ((sortedOutputs.size() % 2) == 1) {
                normalizedPositionMedian = normalizedPosition(sortedOutputs.get(sortedOutputs.size() / 2), bitLength);
            }
            else {
                BigDecimal left = normalizedPosition(sortedOutputs.get((sortedOutputs.size() / 2) - 1), bitLength);
                BigDecimal right = normalizedPosition(sortedOutputs.get(sortedOutputs.size() / 2), bitLength);
                normalizedPositionMedian = left.add(right).divide(BigDecimal.valueOf(2L), STAT_SCALE, RoundingMode.HALF_UP);
            }

            double[] cdfAtDeciles = new double[CDF_DECILES_NUMERATORS.length];
            for (int i = 0; i < CDF_DECILES_NUMERATORS.length; i++) {
                BigInteger threshold = lower.add(
                    range.multiply(BigInteger.valueOf(CDF_DECILES_NUMERATORS[i])).divide(BigInteger.TEN)
                );
                int count = 0;
                for (BigInteger output : sortedOutputs) {
                    if (output.compareTo(threshold) <= 0) {
                        count++;
                    }
                    else {
                        break;
                    }
                }
                cdfAtDeciles[i] = (double) count / sampleCount;
            }

            return new GeneratorSummary(
                sampleCount,
                outputsAboveFullInterval,
                normalizedPositionMean,
                normalizedPositionMedian,
                mean(rawStarts),
                median(rawStarts),
                mean(walkIncrements),
                median(walkIncrements),
                totalRawStartsConsumed,
                totalWalkIncrements,
                totalConcreteFactorRejects,
                primaryIntervalRejects,
                tailIntervalRejects,
                histogramCounts,
                cdfAtDeciles,
                mod30Counts,
                mod210Counts
            );
        }

        private static int[] buildResidueToAdmissibleIndex() {
            int[] mapping = new int[210];
            Arrays.fill(mapping, -1);
            for (int i = 0; i < MOD210_ADMISSIBLE_RESIDUES.length; i++) {
                mapping[MOD210_ADMISSIBLE_RESIDUES[i]] = i;
            }
            return mapping;
        }
    }

    private static final class DriftSummary {
        private final double normalizedHistogramTvd;
        private final double mod30Tvd;
        private final double mod210AdmissibleTvd;
        private final String coarseVisibilityLabel;
        private final String coarseConcentrationLabel;
        private final String dominantMetric;
        private final double dominantMetricTopFiveContributionShare;

        private DriftSummary(
            double normalizedHistogramTvd,
            double mod30Tvd,
            double mod210AdmissibleTvd,
            String coarseVisibilityLabel,
            String coarseConcentrationLabel,
            String dominantMetric,
            double dominantMetricTopFiveContributionShare
        ) {
            this.normalizedHistogramTvd = normalizedHistogramTvd;
            this.mod30Tvd = mod30Tvd;
            this.mod210AdmissibleTvd = mod210AdmissibleTvd;
            this.coarseVisibilityLabel = coarseVisibilityLabel;
            this.coarseConcentrationLabel = coarseConcentrationLabel;
            this.dominantMetric = dominantMetric;
            this.dominantMetricTopFiveContributionShare = dominantMetricTopFiveContributionShare;
        }
    }

    private static final class PanelResult {
        private final PanelConfig config;
        private final FidelityResult fidelity;
        private final GeneratorSummary baseline;
        private final GeneratorSummary dciPrefilter;
        private final DriftSummary drift;

        private PanelResult(
            PanelConfig config,
            FidelityResult fidelity,
            GeneratorSummary baseline,
            GeneratorSummary dciPrefilter,
            DriftSummary drift
        ) {
            this.config = config;
            this.fidelity = fidelity;
            this.baseline = baseline;
            this.dciPrefilter = dciPrefilter;
            this.drift = drift;
        }
    }

    private static final class ChunkedPrimeTable {
        private final List<List<Integer>> chunks;
        private final List<BigInteger> chunkProducts;

        private ChunkedPrimeTable(int limit, int chunkSize, int startExclusive) {
            if (limit <= startExclusive) {
                throw new IllegalArgumentException("limit must be larger than startExclusive");
            }

            List<Integer> filteredPrimes = new ArrayList<Integer>();
            for (int prime : sievePrimes(limit)) {
                if (prime != 2 && prime > startExclusive) {
                    filteredPrimes.add(Integer.valueOf(prime));
                }
            }

            this.chunks = new ArrayList<List<Integer>>();
            this.chunkProducts = new ArrayList<BigInteger>();
            for (int start = 0; start < filteredPrimes.size(); start += chunkSize) {
                List<Integer> chunk = new ArrayList<Integer>(
                    filteredPrimes.subList(start, Math.min(start + chunkSize, filteredPrimes.size()))
                );
                BigInteger product = ONE;
                for (int prime : chunk) {
                    product = product.multiply(BigInteger.valueOf(prime));
                }
                this.chunks.add(Collections.unmodifiableList(chunk));
                this.chunkProducts.add(product);
            }
        }

        private BigInteger findFactor(BigInteger candidate) {
            for (int i = 0; i < chunks.size(); i++) {
                if (candidate.gcd(chunkProducts.get(i)).equals(ONE)) {
                    continue;
                }
                for (int prime : chunks.get(i)) {
                    BigInteger divisor = BigInteger.valueOf(prime);
                    if (candidate.mod(divisor).equals(BigInteger.ZERO)) {
                        return divisor;
                    }
                }
            }
            return null;
        }
    }

    private static final class MetricChange {
        private final String label;
        private final int baselineCount;
        private final int afterCount;
        private final double absoluteProbabilityDelta;

        private MetricChange(String label, int baselineCount, int afterCount, double absoluteProbabilityDelta) {
            this.label = label;
            this.baselineCount = baselineCount;
            this.afterCount = afterCount;
            this.absoluteProbabilityDelta = absoluteProbabilityDelta;
        }
    }

    private static List<Integer> sievePrimes(int limit) {
        if (limit < 2) {
            return List.of();
        }

        byte[] flags = new byte[limit + 1];
        for (int i = 2; i <= limit; i++) {
            flags[i] = 1;
        }

        for (int value = 2; (long) value * value <= limit; value++) {
            if (flags[value] == 0) {
                continue;
            }
            for (int composite = value * value; composite <= limit; composite += value) {
                flags[composite] = 0;
            }
        }

        List<Integer> primes = new ArrayList<Integer>();
        for (int value = 2; value <= limit; value++) {
            if (flags[value] != 0) {
                primes.add(Integer.valueOf(value));
            }
        }
        return primes;
    }
}
