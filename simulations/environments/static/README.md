# Static Environments

## Purpose

The `static/` directory contains **fixed, unchanging environmental configurations** for the brain simulation system. Unlike dynamic scenarios that evolve over time, static environments provide stable sensory inputs and consistent world states for training and evaluation.

## Directory Structure

```
static/
├── README.md                    # This file
├── blueprints/                  # Core environment templates
│   ├── environment_template.py  # Base class for all static environments
│   ├── sensory_field.py         # Sensory input field definitions
│   └── world_state.py           # Static world state management
├── configurations/              # Pre-built environment configs
│   ├── basic_grid.yaml          # Simple 2D grid world
│   ├── feature_field.yaml       # Static feature map
│   └── reward_field.yaml        # Static reward distribution
├── builders/                    # Factory functions for creation
│   ├── grid_builder.py          # Build grid-based environments
│   └── field_builder.py         # Build continuous field environments
└── validation/                  # Verification & testing
    ├── config_validator.py      # Validate environment configs
    └── consistency_checks.py     # Check environment properties
```

## Core Components

### 1. **Environment Templates** (`blueprints/`)

Defines the base structure for all static environments.

#### `environment_template.py`
- Abstract base class: `StaticEnvironment`
- Provides interface for:
  - State initialization
  - Sensory input generation
  - Reward computation
  - State validation

#### `sensory_field.py`
- Representations of static sensory inputs
- Supports:
  - Grid-based inputs (2D/3D grids)
  - Continuous fields (feature maps)
  - Discrete feature sets

#### `world_state.py`
- Manages static world configuration
- Stores:
  - Environment dimensions
  - Fixed features
  - Reward structure
  - Input/output specifications

### 2. **Configurations** (`configurations/`)

YAML-based environment specifications for reproducibility.

#### `basic_grid.yaml`
```yaml
name: "BasicGridWorld"
type: "grid"
dimensions: [10, 10]
sensory_encoding: "one_hot"
reward_model: "discrete"
```

#### `feature_field.yaml`
```yaml
name: "FeatureField"
type: "continuous_field"
dimensions: [100, 100]
feature_channels: 5
encoding: "gaussian"
```

### 3. **Builders** (`builders/`)

Factory functions to construct environments from configs.

#### `grid_builder.py`
- `build_grid_environment()` - Creates grid-based environments
- `validate_grid_config()` - Ensures grid validity

#### `field_builder.py`
- `build_field_environment()` - Creates continuous field environments
- `validate_field_config()` - Ensures field validity

### 4. **Validation** (`validation/`)

Ensures environment correctness and consistency.

#### `config_validator.py`
- Schema validation
- Dimension checks
- Type validation

#### `consistency_checks.py`
- Input/output shape matching
- Reward range validation
- Feature consistency

## Design Principles

1. **Immutability**: Static environments do not change during simulation
2. **Reproducibility**: All configs are stored in YAML/JSON for exact replication
3. **Composability**: Environments can be combined into more complex scenarios
4. **Validation**: All configurations are validated before use
5. **Documentation**: Each environment includes metadata about its properties

## Usage Example

```python
from static.builders import grid_builder
from static.validation import config_validator

# Load and validate config
config = grid_builder.load_config("configurations/basic_grid.yaml")
config_validator.validate(config)

# Build environment
env = grid_builder.build_grid_environment(config)

# Get sensory input
sensory_input = env.get_sensory_input()
reward = env.compute_reward(action)
```

## Integration Points

- **`agents/`**: Agents interact with static environments
- **`sensory_streams/`**: Converts environment outputs to neural signals
- **`scenarios/`**: Static environments may be used within dynamic scenarios
- **`validation/`**: Results compared against baseline static environment behavior

## Future Extensions

- [ ] Hierarchical environment composition
- [ ] Multi-agent static environments
- [ ] Environment randomization (within static bounds)
- [ ] Procedural generation of static configs
