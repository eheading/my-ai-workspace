import { useMemo, useState } from 'react'
import './App.css'

const featureTabs = [
  {
    id: 'radar',
    eyebrow: 'Market Radar',
    title: 'Track global market moves before they become obvious.',
    description:
      'Turn macro signals, sector rotation, and headline velocity into one visual command center for faster daily decisions.',
    bullets: [
      'Real-time market pulse across regions and sectors',
      'Signal clustering that spots unusual momentum early',
      'A clean view for both retail and institutional workflows',
    ],
    metricLabel: 'Signal coverage',
    metricValue: '24/7',
  },
  {
    id: 'briefings',
    eyebrow: 'AI Briefings',
    title: 'Convert noisy financial news into actionable intelligence.',
    description:
      'Summarize market-moving events, detect sentiment shifts, and surface the context behind every suggested move.',
    bullets: [
      'Hourly AI summaries with directional takeaways',
      'News sentiment mapped to watchlists and themes',
      'Digest format built for rapid executive review',
    ],
    metricLabel: 'Briefing cadence',
    metricValue: 'Hourly',
  },
  {
    id: 'models',
    eyebrow: 'Prediction Engine',
    title: 'Blend qualitative AI reasoning with quantitative models.',
    description:
      'Combine OpenAI-assisted analysis with future-ready model pipelines such as XGBoost and LSTM for richer scenario planning.',
    bullets: [
      'Supports short-term thesis validation',
      'Designed for expanding model experimentation',
      'Keeps assumptions visible instead of hiding them',
    ],
    metricLabel: 'Model strategy',
    metricValue: 'Hybrid AI',
  },
  {
    id: 'custom',
    eyebrow: 'Custom Services',
    title: 'Shape the platform around your portfolio, data, and brand.',
    description:
      'Commission tailored dashboards, reporting flows, or investment research experiences that match your audience and operating model.',
    bullets: [
      'Custom data sources and alert logic',
      'Branded interfaces for clients or teams',
      'Fast scoping for white-label and internal products',
    ],
    metricLabel: 'Delivery style',
    metricValue: 'Made-to-order',
  },
]

const outcomes = [
  {
    label: 'Institutional clarity',
    value: 'One cockpit for signals, summaries, and scenarios',
  },
  {
    label: 'Faster decisions',
    value: 'Move from information overload to ranked next actions',
  },
  {
    label: 'Custom engagement',
    value: 'Turn the product into a service offering for your audience',
  },
]

const serviceOptions = [
  'Investor dashboard design',
  'Private strategy workspace',
  'Branded white-label portal',
  'Custom alert pipelines',
  'Executive reporting automation',
]

const riskProfiles = [
  {
    max: 34,
    name: 'Capital Preservation',
    summary: 'Prioritize defense, liquidity, and low-volatility opportunities.',
    focus: ['Defensive sectors', 'High-conviction watchlists', 'Stricter risk filters'],
  },
  {
    max: 69,
    name: 'Balanced Alpha',
    summary: 'Blend resilience with momentum to capture upside without overexposure.',
    focus: ['Cross-sector rotation', 'Event-driven setups', 'Moderate conviction sizing'],
  },
  {
    max: 100,
    name: 'Aggressive Expansion',
    summary: 'Lean into faster-moving opportunities backed by AI-supported conviction.',
    focus: ['High-beta themes', 'Breakout monitoring', 'Short-term tactical entries'],
  },
]

function App() {
  const [activeFeature, setActiveFeature] = useState(featureTabs[0].id)
  const [riskScore, setRiskScore] = useState(58)
  const [selectedServices, setSelectedServices] = useState([
    serviceOptions[0],
    serviceOptions[2],
  ])
  const [copyState, setCopyState] = useState('Copy brief')

  const currentFeature =
    featureTabs.find((feature) => feature.id === activeFeature) ?? featureTabs[0]

  const currentRiskProfile = useMemo(
    () => riskProfiles.find((profile) => riskScore <= profile.max) ?? riskProfiles[1],
    [riskScore],
  )

  const serviceBrief = useMemo(() => {
    const picked = selectedServices.length > 0 ? selectedServices.join(', ') : 'Discovery call'

    return [
      'Custom AI-Investment-Analysis request',
      `Priority services: ${picked}`,
      `Preferred operating mode: ${currentRiskProfile.name}`,
      'Goal: build an English-first, premium investment intelligence experience.',
      'Please contact me through the GitHub project to discuss scope and delivery.',
    ].join('\n')
  }, [currentRiskProfile.name, selectedServices])

  const toggleService = (service) => {
    setSelectedServices((current) =>
      current.includes(service)
        ? current.filter((item) => item !== service)
        : [...current, service],
    )
  }

  const copyBrief = async () => {
    try {
      await navigator.clipboard.writeText(serviceBrief)
      setCopyState('Copied')
      window.setTimeout(() => setCopyState('Copy brief'), 1800)
    } catch {
      setCopyState('Copy failed')
      window.setTimeout(() => setCopyState('Copy brief'), 1800)
    }
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <a className="brand" href="#hero">
          AI-Investment-Analysis
        </a>
        <nav className="nav">
          <a href="#features">Features</a>
          <a href="#simulator">Interactive Demo</a>
          <a href="#services">Custom Service</a>
        </nav>
        <a
          className="ghost-button"
          href="https://github.com/eheading/AI-Investment-Analysis"
          target="_blank"
          rel="noreferrer"
        >
          View Project
        </a>
      </header>

      <main>
        <section className="hero-section" id="hero">
          <div className="hero-copy">
            <span className="eyebrow">AI-powered investment intelligence</span>
            <h1>Launch faster, sharper, and more credible investment decisions.</h1>
            <p className="hero-text">
              AI-Investment-Analysis is a premium investment analysis system designed to
              transform global market data, financial news, and predictive models into a
              beautiful decision cockpit.
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#services">
                Request custom service
              </a>
              <a className="secondary-button" href="#features">
                Explore capabilities
              </a>
            </div>
            <div className="hero-metrics">
              {outcomes.map((outcome) => (
                <article className="metric-card" key={outcome.label}>
                  <span>{outcome.label}</span>
                  <strong>{outcome.value}</strong>
                </article>
              ))}
            </div>
          </div>

          <div className="hero-panel" aria-label="AI market cockpit preview">
            <div className="panel-header">
              <div>
                <span className="eyebrow">Live command preview</span>
                <h2>Designed to look as smart as the analysis feels.</h2>
              </div>
              <div className="status-pill">Momentum +14.8%</div>
            </div>

            <div className="panel-grid">
              <article className="glass-card spotlight-card">
                <span>AI conviction score</span>
                <strong>87 / 100</strong>
                <p>Multi-source reasoning aligned with news flow and technical structure.</p>
              </article>

              <article className="glass-card">
                <span>Headline sentiment</span>
                <strong>Bullish bias</strong>
                <div className="signal-bars" aria-hidden="true">
                  <div />
                  <div />
                  <div />
                  <div />
                </div>
              </article>

              <article className="glass-card">
                <span>Theme rotation</span>
                <ul className="mini-list">
                  <li>AI infrastructure</li>
                  <li>Energy resilience</li>
                  <li>Defensive quality</li>
                </ul>
              </article>

              <article className="glass-card chart-card">
                <span>Signal acceleration</span>
                <div className="chart-line" aria-hidden="true">
                  <span />
                </div>
              </article>
            </div>
          </div>
        </section>

        <section className="feature-section" id="features">
          <div className="section-heading">
            <span className="eyebrow">Core capabilities</span>
            <h2>Every important function, presented like a flagship product.</h2>
            <p>
              This website is built to sell the vision: serious market intelligence,
              beautiful execution, and service-ready customization.
            </p>
          </div>

          <div className="feature-workbench">
            <div className="feature-tabs" role="tablist" aria-label="Feature explorer">
              {featureTabs.map((feature) => (
                <button
                  key={feature.id}
                  className={feature.id === activeFeature ? 'tab-button active' : 'tab-button'}
                  onClick={() => setActiveFeature(feature.id)}
                  role="tab"
                  aria-selected={feature.id === activeFeature}
                  type="button"
                >
                  {feature.eyebrow}
                </button>
              ))}
            </div>

            <article className="feature-display" role="tabpanel">
              <div>
                <span className="eyebrow">{currentFeature.eyebrow}</span>
                <h3>{currentFeature.title}</h3>
                <p>{currentFeature.description}</p>
              </div>

              <div className="feature-insights">
                <div className="highlight-stat">
                  <span>{currentFeature.metricLabel}</span>
                  <strong>{currentFeature.metricValue}</strong>
                </div>

                <ul className="check-list">
                  {currentFeature.bullets.map((bullet) => (
                    <li key={bullet}>{bullet}</li>
                  ))}
                </ul>
              </div>
            </article>
          </div>
        </section>

        <section className="simulator-section" id="simulator">
          <div className="section-heading">
            <span className="eyebrow">Interactive experience</span>
            <h2>Adjust the risk appetite and watch the product story adapt.</h2>
            <p>
              A modern marketing site should do more than scroll. This simulator showcases
              how the platform can personalize insights for different investor profiles.
            </p>
          </div>

          <div className="simulator-card">
            <div className="slider-panel">
              <label htmlFor="risk-score">Risk appetite</label>
              <input
                id="risk-score"
                max="100"
                min="0"
                onChange={(event) => setRiskScore(Number(event.target.value))}
                type="range"
                value={riskScore}
              />
              <div className="slider-scale">
                <span>Conservative</span>
                <strong>{riskScore}</strong>
                <span>Aggressive</span>
              </div>
            </div>

            <article className="simulator-output">
              <span className="eyebrow">Recommended experience</span>
              <h3>{currentRiskProfile.name}</h3>
              <p>{currentRiskProfile.summary}</p>
              <div className="focus-grid">
                {currentRiskProfile.focus.map((item) => (
                  <div className="focus-chip" key={item}>
                    {item}
                  </div>
                ))}
              </div>
            </article>
          </div>
        </section>

        <section className="services-section" id="services">
          <div className="section-heading">
            <span className="eyebrow">Custom engagement</span>
            <h2>Package the system into a bespoke service offer.</h2>
            <p>
              Choose what matters most, generate a collaboration brief, and direct prospects
              to request a tailored build.
            </p>
          </div>

          <div className="services-layout">
            <div className="service-selector">
              {serviceOptions.map((service) => {
                const selected = selectedServices.includes(service)

                return (
                  <button
                    key={service}
                    className={selected ? 'service-chip selected' : 'service-chip'}
                    onClick={() => toggleService(service)}
                    type="button"
                  >
                    {service}
                  </button>
                )
              })}
            </div>

            <article className="brief-card">
              <span className="eyebrow">Generated brief</span>
              <pre>{serviceBrief}</pre>
              <div className="brief-actions">
                <button className="primary-button" onClick={copyBrief} type="button">
                  {copyState}
                </button>
                <a
                  className="secondary-button"
                  href="https://github.com/eheading/AI-Investment-Analysis/issues/new"
                  target="_blank"
                  rel="noreferrer"
                >
                  Request via GitHub
                </a>
              </div>
            </article>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>Built as an English-first premium landing page for AI-Investment-Analysis.</p>
        <a href="#hero">Back to top</a>
      </footer>
    </div>
  )
}

export default App
