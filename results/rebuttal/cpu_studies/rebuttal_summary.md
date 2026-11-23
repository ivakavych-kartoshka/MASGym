# MASGym Rebuttal Studies Summary (CPU-only, Seed-locked)

## Study 1A: Availability-Rule Ablation on N=5, M=30 Grid (0%-Compliance Defended Regime)
| topology | scenario | asr_sys_full_0pct_comp | ci_full | asr_sys_no_hub_rule_0pct_comp | ci_no_hub | hub_rule_only_share |
| --- | --- | --- | --- | --- | --- | --- |
| star | single_attacker | 0.8333 | [0.664, 0.927] | 0.3 | [0.167, 0.479] | 0.5333 |
| star | colluding | 1.0 | [0.886, 1.000] | 0.3 | [0.167, 0.479] | 0.7 |
| star | compromised_orchestrator | 1.0 | [0.886, 1.000] | 0.2333 | [0.118, 0.409] | 0.7667 |
| chain | single_attacker | 0.1 | [0.035, 0.256] | 0.1 | [0.035, 0.256] | 0.0 |
| chain | colluding | 0.0 | [0.000, 0.114] | 0.0 | [0.000, 0.114] | 0.0 |
| chain | compromised_orchestrator | 0.1 | [0.035, 0.256] | 0.1 | [0.035, 0.256] | 0.0 |
| tree | single_attacker | 0.3 | [0.167, 0.479] | 0.0333 | [0.006, 0.167] | 0.2667 |
| tree | colluding | 1.0 | [0.886, 1.000] | 0.3 | [0.167, 0.479] | 0.7 |
| tree | compromised_orchestrator | 1.0 | [0.886, 1.000] | 0.1667 | [0.073, 0.336] | 0.8333 |
| mesh | single_attacker | 0.7 | [0.521, 0.833] | 0.7 | [0.521, 0.833] | 0.0 |
| mesh | colluding | 0.4333 | [0.274, 0.608] | 0.4333 | [0.274, 0.608] | 0.0 |
| mesh | compromised_orchestrator | 0.5333 | [0.361, 0.698] | 0.5333 | [0.361, 0.698] | 0.0 |

## Study 1B: Availability-Rule Ablation on Synthetic Degradation (M=738, Star N=5, beta=0.3)
| context | defense | asr_sys_full | asr_sys_no_hub_rule | asr_act | quorum_only_sabotage |
| --- | --- | --- | --- | --- | --- |
| ma_colluding | no_defense | 1.0 | 0.6572 | 0.5745 | 0.0827 |
| ma_colluding | per_agent_guardrail | 1.0 | 0.4241 | 0.3699 | 0.0542 |
| ma_colluding | system_fixed_threshold | 1.0 | 0.5393 | 0.4648 | 0.0745 |
| ma_comp_orch | no_defense | 1.0 | 0.6369 | 0.5556 | 0.0813 |
| ma_comp_orch | per_agent_guardrail | 1.0 | 0.3984 | 0.3496 | 0.0488 |
| ma_comp_orch | system_fixed_threshold | 1.0 | 0.5407 | 0.4743 | 0.0664 |

## Study 2A: Controlled Collusion (FIXED s=2 Attackers & FIXED Placement, M=738)
| topology | placement | cpr_shared | asr_act_ind | asr_act_coord | delta_effort | delta_effort_ci | p_effort_holm | split_ind | split_coord | delta_split | p_split_holm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chain | random | 0.1125 | 0.3415 | 0.6138 | 0.2724 | [+0.240, +0.304] | 0.0016 | 0.0474 | 0.1558 | 0.1084 | 0.0016 |
| chain | central | 0.1373 | 0.3401 | 0.6328 | 0.2927 | [+0.260, +0.327] | 0.0016 | 0.061 | 0.1653 | 0.1043 | 0.0016 |
| tree | random | 0.1251 | 0.3523 | 0.622 | 0.2696 | [+0.237, +0.302] | 0.0016 | 0.0596 | 0.1653 | 0.1057 | 0.0016 |
| tree | central | 0.2972 | 0.3537 | 0.6599 | 0.3062 | [+0.272, +0.340] | 0.0016 | 0.0881 | 0.229 | 0.1409 | 0.0016 |
| star | random | 0.2836 | 0.3672 | 0.6626 | 0.2954 | [+0.262, +0.328] | 0.0016 | 0.0799 | 0.2222 | 0.1423 | 0.0016 |
| star | central | 0.2818 | 0.336 | 0.6694 | 0.3333 | [+0.298, +0.367] | 0.0016 | 0.0678 | 0.2249 | 0.1572 | 0.0016 |
| mesh | random | 0.6522 | 0.3442 | 0.7724 | 0.4282 | [+0.393, +0.465] | 0.0016 | 0.1125 | 0.3442 | 0.2317 | 0.0016 |
| mesh | central | 0.6653 | 0.355 | 0.7561 | 0.4011 | [+0.367, +0.435] | 0.0016 | 0.1301 | 0.3388 | 0.2087 | 0.0016 |

## Study 2B: Placement-Only Effect (s=1 Independent Seed, Random vs Central, M=738)
| topology | cpr_random_place | cpr_central_place | delta_place_cpr | ci_95 |
| --- | --- | --- | --- | --- |
| chain | 0.0708 | 0.1033 | 0.0325 | [+0.016, +0.050] |
| tree | 0.0742 | 0.208 | 0.1338 | [+0.112, +0.154] |
| star | 0.1762 | 0.2981 | 0.122 | [+0.098, +0.147] |
| mesh | 0.5295 | 0.4973 | -0.0322 | [-0.072, +0.007] |

## Study 3: Propagation Sensitivity & Alternative Models (N=5, beta=0.3, M=738)
| topology | model_family | parameter | cpr | final_compromised_frac | quorum_avail_fail |
| --- | --- | --- | --- | --- | --- |
| chain | threshold | theta=1 | 0.6608 | 0.7965 | 0.6965 |
| chain | threshold | theta=2 | 0.0 | 0.4 | 0.0 |
| chain | threshold | theta=3 | 0.0 | 0.4 | 0.0 |
| chain | independent_cascade | p=0.1 | 0.0361 | 0.4217 | 0.0081 |
| chain | independent_cascade | p=0.3 | 0.1355 | 0.4813 | 0.0745 |
| chain | independent_cascade | p=0.5 | 0.2665 | 0.5599 | 0.2141 |
| chain | linear_threshold | uniform_U(0,1) | 0.6581 | 0.7949 | 0.6911 |
| tree | threshold | theta=1 | 0.5316 | 0.719 | 0.5 |
| tree | threshold | theta=2 | 0.0 | 0.4 | 0.0 |
| tree | threshold | theta=3 | 0.0 | 0.4 | 0.0 |
| tree | independent_cascade | p=0.1 | 0.0384 | 0.423 | 0.0122 |
| tree | independent_cascade | p=0.3 | 0.1323 | 0.4794 | 0.0745 |
| tree | independent_cascade | p=0.5 | 0.2331 | 0.5398 | 0.1978 |
| tree | linear_threshold | uniform_U(0,1) | 0.5239 | 0.7144 | 0.4946 |
| star | threshold | theta=1 | 1.0 | 1.0 | 1.0 |
| star | threshold | theta=2 | 0.2028 | 0.5217 | 0.0 |
| star | threshold | theta=3 | 0.0 | 0.4 | 0.0 |
| star | independent_cascade | p=0.1 | 0.0894 | 0.4537 | 0.0407 |
| star | independent_cascade | p=0.3 | 0.29 | 0.574 | 0.2642 |
| star | independent_cascade | p=0.5 | 0.5018 | 0.7011 | 0.5461 |
| star | linear_threshold | uniform_U(0,1) | 0.6816 | 0.8089 | 0.6816 |
| mesh | threshold | theta=1 | 1.0 | 1.0 | 1.0 |
| mesh | threshold | theta=2 | 1.0 | 1.0 | 1.0 |
| mesh | threshold | theta=3 | 0.0 | 0.4 | 0.0 |
| mesh | independent_cascade | p=0.1 | 0.2285 | 0.5371 | 0.1775 |
| mesh | independent_cascade | p=0.3 | 0.6802 | 0.8081 | 0.7195 |
| mesh | independent_cascade | p=0.5 | 0.9051 | 0.9431 | 0.9526 |
| mesh | linear_threshold | uniform_U(0,1) | 0.7963 | 0.8778 | 0.7629 |

## Study 3 (continued): N=10, beta=0.3, M=738
| topology | model_family | parameter | cpr | final_compromised_frac | quorum_avail_fail |
| --- | --- | --- | --- | --- | --- |
| chain | threshold | theta=1 | 0.6947 | 0.7863 | 0.4011 |
| chain | threshold | theta=2 | 0.0 | 0.3 | 0.0 |
| chain | threshold | theta=3 | 0.0 | 0.3 | 0.0 |
| chain | independent_cascade | p=0.1 | 0.0337 | 0.3236 | 0.0 |
| chain | independent_cascade | p=0.3 | 0.1055 | 0.3738 | 0.0 |
| chain | independent_cascade | p=0.5 | 0.2232 | 0.4562 | 0.0081 |
| chain | linear_threshold | uniform_U(0,1) | 0.6847 | 0.7793 | 0.3388 |
| tree | threshold | theta=1 | 0.507 | 0.6549 | 0.3144 |
| tree | threshold | theta=2 | 0.0 | 0.3 | 0.0 |
| tree | threshold | theta=3 | 0.0 | 0.3 | 0.0 |
| tree | independent_cascade | p=0.1 | 0.0341 | 0.3238 | 0.0 |
| tree | independent_cascade | p=0.3 | 0.1022 | 0.3715 | 0.0014 |
| tree | independent_cascade | p=0.5 | 0.2079 | 0.4455 | 0.0149 |
| tree | linear_threshold | uniform_U(0,1) | 0.506 | 0.6542 | 0.3401 |
| star | threshold | theta=1 | 1.0 | 1.0 | 1.0 |
| star | threshold | theta=2 | 0.097 | 0.3679 | 0.0 |
| star | threshold | theta=3 | 0.1009 | 0.3706 | 0.0 |
| star | independent_cascade | p=0.1 | 0.0763 | 0.3534 | 0.0 |
| star | independent_cascade | p=0.3 | 0.2778 | 0.4944 | 0.0068 |
| star | independent_cascade | p=0.5 | 0.5006 | 0.6504 | 0.084 |
| star | linear_threshold | uniform_U(0,1) | 0.4919 | 0.6443 | 0.4919 |
| mesh | threshold | theta=1 | 1.0 | 1.0 | 1.0 |
| mesh | threshold | theta=2 | 1.0 | 1.0 | 1.0 |
| mesh | threshold | theta=3 | 1.0 | 1.0 | 1.0 |
| mesh | independent_cascade | p=0.1 | 0.4111 | 0.5878 | 0.107 |
| mesh | independent_cascade | p=0.3 | 0.9437 | 0.9606 | 0.9309 |
| mesh | independent_cascade | p=0.5 | 0.9973 | 0.9981 | 0.9986 |
| mesh | linear_threshold | uniform_U(0,1) | 0.7567 | 0.8297 | 0.607 |

## Study 4A: Table 1 Episode-Level & Cluster-Aware CI Reconciliation
| quantity | k | n | point | wilson_95_two_sided | wilson_bonf12_95 | exact_cp_95 |
| --- | --- | --- | --- | --- | --- | --- |
| cell_0_of_30 (chain/mesh 0.00) | 0 | 30 | 0.0 | [0.0000, 0.1135] | [0.0000, 0.2149] | [0.0000, 0.1157] |
| cell_13_of_30 (mesh coll 0.43) | 13 | 30 | 0.4333 | [0.2738, 0.6080] | [0.2175, 0.6778] | [0.2738, 0.6080] |
| cell_30_of_30 (tree/star 1.00) | 30 | 30 | 1.0 | [0.8865, 1.0000] | [0.7851, 1.0000] | [0.8843, 1.0000] |
| pooled_360_episodes_0_of_360 (cluster-level) | 0 | 360 | 0.0 | [0.0000, 0.0106] | [0.0000, 0.0223] | [0.0000, 0.0102] |
| pooled_1075_decisions_naive_iid (for contrast) | 0 | 1075 | 0.0 | [0.0000, 0.0036] | [0.0000, 0.0076] | [0.0000, 0.0034] |

## Study 4B: Real Llama-3.2-1B (Undefended) Pooled Cluster Summary
{
  "pooled_decisions": 1075,
  "pooled_exfil": 1075,
  "n_episodes_pooled": 360,
  "mean_decisions_per_episode": 2.986,
  "effective_n_under_icc1": 360,
  "defended_0pct_cluster_wilson_95_upper": 0.0106,
  "defended_0pct_cluster_bonf4_upper": 0.017
}

## Study 4C: Synthetic Action-Channel Degradation Bootstrap CIs (M=738)
| context | asr_act_none | asr_act_guard | abs_reduction | abs_ci_95 | rel_reduction_pct | rel_ci_95_pct |
| --- | --- | --- | --- | --- | --- | --- |
| single_agent_ASB | 0.5691 | 0.3306 | 0.2385 | [0.188, 0.287] | 41.9 | [34.6%, 48.6%] |
| ma_colluding | 0.5528 | 0.3713 | 0.1816 | [0.130, 0.230] | 32.8 | [24.6%, 40.1%] |
| ma_comp_orch | 0.5515 | 0.3496 | 0.2019 | [0.152, 0.252] | 36.6 | [28.8%, 43.9%] |

### Cross-Context Shrinkage Bootstrap Tests
| comparison | rel_shrinkage_pp | ci_95_pp | p_boot_two_sided |
| --- | --- | --- | --- |
| single_agent -> ma_colluding | 9.1 | [-1.2pp, +19.9pp] | 0.0826 |
| single_agent -> ma_comp_orch | 5.3 | [-4.7pp, +15.5pp] | 0.2918 |
