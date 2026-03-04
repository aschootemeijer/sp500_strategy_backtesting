import matplotlib.pyplot as plt

def plot_price_vs_time( d, dr, ax, ticker ):
    ax.plot( dr.Date, dr.Close/max(d.Close), alpha=1, lw=1.3, label=ticker)
    ax.plot( d.Date, d.Close/max(d.Close), alpha=0.29, c='grey', lw=0.8, zorder=-1 )

s = 12
def prettify_and_show( ax1,ax2,strategy,strategy_yrly_incr,control_yrly_incr ):
    for ax in [ax1, ax2]:
        ax.set_xlabel( 'Time', size=s+2 )
        ax.tick_params( 'x', rotation=30)
        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params( axis='both',direction='in')
    ax1.text( 0.025, 0.975, f'{strategy} stocks.\nAVG: {strategy_yrly_incr}%/yr', transform=ax1.transAxes, va='top', ha='left', size=s )
    ax2.text( 0.025, 0.975, f'control stocks.\nAVG: {control_yrly_incr}%/yr',    transform=ax2.transAxes, va='top', ha='left', size=s )
    ax1.set_ylabel( 'Stock value (norm. to max)', size=s+2 )    
    plt.tight_layout()
    plt.show()

