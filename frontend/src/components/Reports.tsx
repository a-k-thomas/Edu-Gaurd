import React from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  Avatar,
  LinearProgress,
  useTheme,
  alpha,
} from '@mui/material'
import {
  AssessmentRounded as AssessmentIcon,
  TrendingDownRounded as TrendingDownIcon,
  SchoolRounded as SchoolIcon,
  CheckCircleOutlineRounded as SafeIcon,
  FileDownloadRounded as ExportIcon,
  PrintRounded as PrintIcon,
  WarningAmberRounded as WarningIcon,
  LightbulbRounded as InsightIcon,
} from '@mui/icons-material'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

const riskByClassData = [
  { class: 'Class 8', high: 1, medium: 3, low: 6 },
  { class: 'Class 9', high: 1, medium: 4, low: 5 },
  { class: 'Class 10', high: 2, medium: 5, low: 3 },
  { class: 'Class 11', high: 1, medium: 4, low: 5 },
  { class: 'Class 12', high: 0, medium: 3, low: 7 },
]

const factorData = [
  { name: 'Low Attendance (<70%)', count: 18, pct: 36, color: '#f43f5e' },
  { name: 'Academic Underperformance', count: 14, pct: 28, color: '#f59e0b' },
  { name: 'Economic / Income Stress', count: 12, pct: 24, color: '#6366f1' },
  { name: 'No Digital Device at Home', count: 9, pct: 18, color: '#06b6d4' },
  { name: 'Health-Related Absences', count: 7, pct: 14, color: '#ec4899' },
]

export const Reports: React.FC = () => {
  const theme = useTheme()
  const isLight = theme.palette.mode === 'light'

  const handlePrint = () => {
    window.print()
  }

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      {/* Top Header */}
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', alignItems: { sm: 'center' }, gap: 2, mb: 3 }}>
        <Box>
          <Typography variant="h2" sx={{ fontWeight: 800, mb: 0.5 }}>
            Analytics & Cohort Reports
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Cross-sectional vulnerability evaluation, classroom breakdown, and intervention success tracking.
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1.5 }}>
          <Button
            variant="outlined"
            onClick={handlePrint}
            startIcon={<PrintIcon />}
            sx={{ fontWeight: 600 }}
          >
            Print Overview
          </Button>
          <Button
            variant="contained"
            onClick={() => alert('Comprehensive CSV dataset exported successfully!')}
            startIcon={<ExportIcon />}
            sx={{ fontWeight: 700 }}
          >
            Export CSV Dataset
          </Button>
        </Box>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={2.5} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Box>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 700, textTransform: 'uppercase' }}>
                    Active Cases Monitored
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: 800, mt: 0.5 }}>
                    24
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: alpha('#f59e0b', 0.12), color: '#f59e0b' }}>
                  <AssessmentIcon />
                </Avatar>
              </Box>
              <Chip label="High & Med Risk Subgroups" size="small" sx={{ fontWeight: 600, fontSize: '0.7rem' }} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Box>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 700, textTransform: 'uppercase' }}>
                    Intervention Success Rate
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: 800, mt: 0.5, color: '#10b981' }}>
                    76.4%
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: alpha('#10b981', 0.12), color: '#10b981' }}>
                  <SafeIcon />
                </Avatar>
              </Box>
              <Chip label="+4.2% from Last Term" size="small" sx={{ bgcolor: alpha('#10b981', 0.1), color: '#059669', fontWeight: 700, fontSize: '0.7rem' }} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Box>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 700, textTransform: 'uppercase' }}>
                    Dropouts Averted
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: 800, mt: 0.5, color: 'primary.main' }}>
                    19
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: alpha(theme.palette.primary.main, 0.1), color: theme.palette.primary.main }}>
                  <SchoolIcon />
                </Avatar>
              </Box>
              <Chip label="Preventative Counseling" size="small" sx={{ fontWeight: 600, fontSize: '0.7rem' }} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Box>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 700, textTransform: 'uppercase' }}>
                    Critical Watchlist
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: 800, mt: 0.5, color: '#f43f5e' }}>
                    5
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: alpha('#f43f5e', 0.12), color: '#f43f5e' }}>
                  <WarningIcon />
                </Avatar>
              </Box>
              <Chip label="Immediate Counselor Allotment" size="small" sx={{ bgcolor: alpha('#f43f5e', 0.1), color: '#f43f5e', fontWeight: 700, fontSize: '0.7rem' }} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Visual Analytics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Risk by Class Bar Chart */}
        <Grid item xs={12} lg={7}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  Cohort Vulnerability Distribution by Class
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Comparative stack of high, medium, and low risk allocations across Grades 8 through 12
                </Typography>
              </Box>

              <Box sx={{ height: 300, width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={riskByClassData} margin={{ top: 15, right: 15, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isLight ? '#f1f5f9' : '#1e293b'} vertical={false} />
                    <XAxis dataKey="class" stroke={isLight ? '#94a3b8' : '#64748b'} fontSize={12} tickLine={false} />
                    <YAxis stroke={isLight ? '#94a3b8' : '#64748b'} fontSize={12} tickLine={false} />
                    <RechartsTooltip
                      contentStyle={{
                        borderRadius: 12,
                        backgroundColor: isLight ? 'rgba(255, 255, 255, 0.95)' : '#1f2937',
                        borderColor: isLight ? '#e2e8f0' : '#374151',
                        boxShadow: '0 8px 20px rgba(0,0,0,0.15)',
                      }}
                    />
                    <Legend />
                    <Bar dataKey="high" name="High Risk" fill="#f43f5e" stackId="a" radius={[0, 0, 0, 0]} />
                    <Bar dataKey="medium" name="Medium Risk" fill="#f59e0b" stackId="a" radius={[0, 0, 0, 0]} />
                    <Bar dataKey="low" name="Low Risk (Safe)" fill="#10b981" stackId="a" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Contributing Risk Factors Breakdown */}
        <Grid item xs={12} lg={5}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  Primary Risk Triggers Across Cohort
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Frequency of compound indicators identified by AI surveillance
                </Typography>
              </Box>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 3 }}>
                {factorData.map((f) => (
                  <Box key={f.name}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.8 }}>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {f.name}
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: f.color }}>
                        {f.count} students ({f.pct}%)
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={f.pct}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        bgcolor: alpha(f.color, 0.15),
                        '& .MuiLinearProgress-bar': {
                          bgcolor: f.color,
                          borderRadius: 4,
                        },
                      }}
                    />
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Key Insights Box */}
      <Card sx={{ p: 1, bgcolor: alpha(theme.palette.primary.main, 0.04), border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}` }}>
        <CardContent sx={{ p: 2.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
            <InsightIcon color="primary" />
            <Typography variant="h5" sx={{ fontWeight: 700 }}>
              AI Analytical Takeaways & Recommendations
            </Typography>
          </Box>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, lineHeight: 1.6 }}>
            • <strong>Class 10 Transition Vuln:</strong> Class 10 exhibits the highest concentration of high-risk flags (20% of class cohort), largely driven by post-midterm academic pressure coupled with irregular attendance.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, lineHeight: 1.6 }}>
            • <strong>Digital Accessibility Impact:</strong> Students lacking home digital devices demonstrate a 2.4x higher probability of falling into the high-risk bracket due to delayed homework submissions.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
            • <strong>Suggested Action:</strong> Initiate targeted tutoring in Science & Mathematics for Class 10 and deploy the school device lending library before next quarter.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}
