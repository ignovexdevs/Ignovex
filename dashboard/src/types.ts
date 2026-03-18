export type RiskLevel = "DISTRIBUTED" | "MODERATE" | "CONCENTRATED" | "DOMINATED";

export interface SignalResult {
  name:      string;
  score:     number;
  triggered: boolean;
  detail:    string;
  weight:    number;
}

export interface ConcentrationReport {
  risk_level:     RiskLevel;
  risk_score:     number;
  signals:        SignalResult[];
  recommendation: string;
  timestamp:      number;
}
