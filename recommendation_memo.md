# Executive Recommendation Memo

**To:** Senior Leadership, Customer Retention Division  
**From:** Executive Analytics Capstone Internship Team  
**Date:** November 24, 2026  
**Re:** Customer Segmentation & Churn-Risk Prioritization — Action Plan

---

## Purpose

This memo summarizes the customer segmentation and risk-scoring analysis completed on 10,000 telecom customers and provides prioritized, segment-specific retention recommendations. The analysis uses **explainable, rule-based methods** (no black-box models) to ensure transparency and stakeholder trust.

---

## Key Finding: Four Distinct Customer Segments

| Priority | Segment | Customers | Avg Risk | Historical Churn | Primary Risk Drivers |
|----------|---------|-----------|----------|------------------|---------------------|
| **1 (Highest)** | Senior Vulnerable | 1,546 (15.5%) | 47.0 | 75.0% | Senior status, month-to-month, electronic check, no security |
| **2** | Budget-Conscious | 3,151 (31.5%) | 45.1 | 75.3% | Month-to-month, mailed check, low tenure |
| **3** | High-Value Long-Term | 2,343 (23.4%) | 41.6 | 76.2% | High charges, month-to-month, electronic check |
| **4 (Lowest)** | New Vulnerable | 2,960 (29.6%) | 38.2 | 74.0% | Low tenure, month-to-month, no security |

---

## Priority 1: Senior Vulnerable Customers (1,546 customers)

**Why prioritize:** Highest average risk score (47.0), 25.9% in High Risk category, all are senior citizens with multiple risk factors.

**Recommended Actions:**
1. **Dedicated Senior Support Line** — Establish a specialized support channel with trained agents for senior customers.
2. **Contract Upgrade Incentive** — Offer 20% discount on first year of annual contract for month-to-month seniors.
3. **Automatic Payment Migration** — Waive setup fees and provide guided assistance to switch from electronic check to bank transfer/credit card auto-pay.
4. **Security Bundle** — Include online security free for 12 months with any contract upgrade.
5. **Proactive Outreach** — Quarterly check-in calls (not automated) for all High Risk seniors.

**Expected Impact:** Addresses 4 of 7 risk factors simultaneously. Even 10% retention uplift = ~115 customers saved.

---

## Priority 2: Budget-Conscious Customers (3,151 customers)

**Why prioritize:** Largest segment (31.5% of base), high risk scores driven by contract type and payment method.

**Recommended Actions:**
1. **Value Plan Introduction** — Launch a "Essentials" tier at $45/month with core services for price-sensitive customers.
2. **Annual Commitment Discount** — 15% off monthly rate for 1-year commitment (effective $50.60/mo vs $59.49 current).
3. **Payment Method Nudge** — Email/SMS campaign highlighting convenience and security of auto-pay; $5/month credit for 3 months after switching.
4. **Usage Alerts** — Proactive notifications when approaching data/minute limits to prevent bill shock.

**Expected Impact:** Largest addressable population. 5% retention uplift = ~118 customers saved.

---

## Priority 3: High-Value Long-Term Customers (2,343 customers)

**Why prioritize:** Highest revenue per customer ($5,092 lifetime), but 76.2% historical churn — losing these is costly.

**Recommended Actions:**
1. **Loyalty Recognition Program** — Tiered rewards (silver/gold/platinum) based on tenure; visible in billing portal.
2. **Price Protection Guarantee** — Lock current rate for 24 months with contract renewal.
3. **Dedicated Account Manager** — For top 20% by tenure/charges; single point of contact for issues.
4. **Security & Value-Adds** — Premium security suite included; free device upgrade every 24 months.
5. **Win-Back Protocol** — Immediate escalation path if cancellation requested; authorized retention offers up to 30% discount.

**Expected Impact:** Highest revenue protection. Each retained customer = ~$1,100/year revenue preserved.

---

## Priority 4: New Vulnerable Customers (2,960 customers)

**Why prioritize:** Early intervention opportunity — low tenure (28 months avg) means onboarding gaps can be fixed.

**Recommended Actions:**
1. **Structured Onboarding Journey** — 30/60/90 day touchpoints: welcome call, feature tutorial, satisfaction survey.
2. **Security Default-On** — Enable online security by default for new customers (opt-out vs opt-in).
3. **First-Year Contract Incentive** — Month 1-3: month-to-month flexibility; Month 4: auto-convert to 1-year at 10% discount unless opted out.
4. **Digital Self-Service** — In-app chatbot for common issues; reduce friction for digital-native customers.
5. **Early Warning System** — Flag customers with >2 support tickets in first 90 days for proactive outreach.

**Expected Impact:** Prevents early churn cascade. Onboarding improvements compound over customer lifetime.

---

## Cross-Segment Quick Wins (Implement Immediately)

| Action | Effort | Impact | Timeline |
|--------|--------|--------|----------|
| Migrate all electronic check → auto-pay | Low | High | 30 days |
| Enable online security by default | Low | Medium | 14 days |
| Add risk score to CRM for support agents | Medium | High | 60 days |
| Monthly segment-level churn dashboard | Low | Medium | 30 days |

---

## Investment vs. Return Estimate

| Initiative | Est. Cost | Customers at Risk | Est. Retained (10% uplift) | Annual Revenue Saved |
|------------|-----------|-------------------|---------------------------|---------------------|
| Senior program | $150K | 400 (High Risk) | 40 | ~$350K |
| Budget value plan | $200K | 750 (High Risk) | 75 | ~$540K |
| Loyalty program | $300K | 310 (High Risk) | 31 | ~$850K |
| Onboarding overhaul | $100K | 370 (High Risk) | 37 | ~$270K |
| **Total** | **$750K** | **1,830** | **183** | **~$2.0M** |

*Assumes avg annual revenue $1,100/customer (High-Value) to $700 (others). Conservative 10% uplift on High Risk only.*

---

## Risk Score Operationalization

**Immediate (Week 1-2):**
- Add `Risk_Score` and `Risk_Category` fields to CRM/customer database
- Train support team on risk factor explanations (see Scoring Methodology)

**Short-term (Month 1):**
- Build automated daily risk scoring for new customers
- Create segment-level retention dashboards for team leads

**Medium-term (Quarter 1):**
- A/B test retention offers by segment
- Validate risk score against actual 90-day churn outcomes
- Calibrate thresholds based on business results

---

## Caveats & Limitations

1. **Not a prediction** — Risk scores are heuristic, not probabilities. A "High Risk" customer may not churn; a "Low Risk" customer may.
2. **Historical churn is 75% overall** — This is unusually high. Validate segment churn rates against current production data.
3. **No causal evidence** — Changing a risk factor (e.g., adding security) may not reduce churn. Test before scaling.
4. **Static snapshot** — Refresh segments and scores quarterly with new data.
5. **External factors** — Competitor actions, economic conditions, life events not captured.

---

## Next Steps & Decisions Required

| Decision | Owner | Deadline |
|----------|-------|----------|
| Approve pilot budget ($750K) | VP Retention | Dec 1 |
| Assign segment ownership to team leads | Dir. Customer Success | Dec 1 |
| Integrate risk scores into CRM | IT / Analytics | Jan 15 |
| Design A/B test framework | Analytics | Jan 15 |
| Quarterly model refresh schedule | Analytics | Ongoing |

---

## Appendix: Scoring Logic Summary (for Stakeholder Communication)

> "Each customer receives a 0-100 risk score based on 7 transparent factors:
> - **Short tenure** (up to 25 pts)
> - **High monthly bill** (up to 20 pts)
> - **Month-to-month contract** (up to 25 pts)
> - **Manual payment method** (up to 10 pts)
> - **No online security** (up to 10 pts)
> - **Senior citizen** (5 pts)
> - **No partner/dependents** (5 pts)
> 
> Scores ≥60 = High Risk (priority outreach), 35-59 = Medium Risk (monitor), <35 = Low Risk (standard care).
> 
> This is not a prediction — it's a prioritization tool to focus limited retention resources where they're most needed."

---

*End of Memo*