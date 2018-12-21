Name:           firecracker
Version:        0.12.0
Release:        2
Summary:        Virtualization software for running multi-tenant containers
License:        Apache-2.0
URL:            https://github.com/firecracker-microvm/firecracker
Source0:        https://github.com/firecracker-microvm/firecracker/archive/v0.12.0/firecracker-v0.12.0.tar.gz
Source1:        http://localhost/cgit/projects/firecracker-vendor/snapshot/firecracker-vendor-v0.12.0.tar.gz

BuildRequires:  musl
BuildRequires:  cargo
BuildRequires:  rustc

%description
Virtualization software for running multi-tenant containers


%prep

# vendored crates
%setup -q -n firecracker-vendor-v0.12.0 -T -b 1

# firecracker sources
%setup -q

# TODO: package these dependencies for the distribution
mkdir -p .cargo
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/../firecracker-vendor-v0.12.0'
EOF

%install
# use our offline registry
export CARGO_HOME=$PWD/.cargo

# Enable optimization, debuginfo, and link hardening.
export RUSTFLAGS="-C opt-level=3 -g -Clink-args=-Wl,-z,relro,-z,now"

cargo install --root %{buildroot}/usr --path . --features vsock

# Remove installer artifacts
rm %{buildroot}/usr/.crates.toml

%files
/usr/bin/firecracker
/usr/bin/jailer
